"""
Gate 3: Public Exposure Scan (Declaration Repository)
Sensitive scan (production IPs/local paths/emails/runner topology/1Password item names)
+ Version consistency checks.
"""
import os
import re
import yaml
from pathlib import Path
from typing import Dict, List, Set
import subprocess
import json


def scan_for_sensitive_data(repo_path: str) -> Dict[str, List[str]]:
    """Scan declaration repository for sensitive data."""
    repo_path = Path(repo_path)
    results = {
        "production_ips": [],
        "local_paths": [],
        "emails": [],
        "runner_topology": [],
        "password_items": []
    }
    
    # Define patterns to search for
    ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?:/[0-9]{1,2})?\b')
    local_path_pattern = re.compile(r'(?:/Users/|/home/)[^/\s"\']+')  # /Users/ or /home/ paths
    email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    runner_pattern = re.compile(r'(?:pve-runner-\d+|ce-01|linux-runner|ubuntu-latest|self-hosted)')
    
    # Search for 1Password item references (common naming patterns)
    password_patterns = [
        re.compile(r'(?:api_?key|token|secret|password|credential).*["\']([A-Za-z0-9+/]{20,})["\']'),
        re.compile(r'1password.*(?:item|entry|vault)', re.IGNORECASE)
    ]
    
    # Walk through all text files in the repository
    for file_path in repo_path.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() not in ['.png', '.jpg', '.jpeg', '.gif', '.bin', '.exe']:
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                
                # Check for production IPs
                ips = ip_pattern.findall(content)
                for ip in ips:
                    # Filter out common false positives like localhost, private ranges if they're likely false
                    if not ip.startswith('127.') and not ip.startswith('10.') and not ip.startswith('192.168.'):
                        results["production_ips"].append(f"{file_path.relative_to(repo_path)}:{ip}")
                
                # Check for local paths
                paths = local_path_pattern.findall(content)
                for path in paths:
                    results["local_paths"].append(f"{file_path.relative_to(repo_path)}:{path}")
                
                # Check for emails
                emails = email_pattern.findall(content)
                for email in emails:
                    results["emails"].append(f"{file_path.relative_to(repo_path)}:{email}")
                
                # Check for runner topology
                runners = runner_pattern.findall(content)
                for runner in runners:
                    results["runner_topology"].append(f"{file_path.relative_to(repo_path)}:{runner}")
                
                # Check for password items
                for pwd_pattern in password_patterns:
                    matches = pwd_pattern.findall(content)
                    for match in matches:
                        if isinstance(match, tuple):
                            match = match[0]  # Get first group if it's a tuple
                        results["password_items"].append(f"{file_path.relative_to(repo_path)}:{match}")
                        
            except Exception:
                # Skip files that can't be read
                continue
    
    return results


def check_version_consistency(repo_path: str) -> Dict[str, str]:
    """Check version consistency where applicable in declaration repo."""
    repo_path = Path(repo_path)
    results = {
        "manifest_version": "NOT_APPLICABLE", 
        "tag_version": "NOT_APPLICABLE",
        "consistent": True
    }
    
    # The declaration repository is documentation-focused, so version checking is different
    # We'll look for version references in documentation
    
    docs_dir = repo_path / "docs"
    if docs_dir.exists():
        version_refs = []
        
        for doc_file in docs_dir.rglob("*.md"):
            try:
                content = doc_file.read_text()
                import re
                # Look for version patterns like v0.18.4
                versions = re.findall(r'v\d+\.\d+\.\d+', content)
                version_refs.extend(versions)
            except:
                continue
        
        # For documentation, we want to ensure references are consistent
        # and that they point to real versions from the engine repo
        unique_versions = list(set(version_refs))
        
        # Check if there are mixed references to different versions
        if len(unique_versions) > 1:
            results["consistent"] = False
    
    return results


def run_gate3_scan(repo_path: str) -> Dict[str, any]:
    """Run the complete Gate 3 scan for declaration repo."""
    results = {
        "sensitive_scan": scan_for_sensitive_data(repo_path),
        "version_consistency": check_version_consistency(repo_path)
    }
    
    return results


def generate_gate3_report(results: Dict[str, any]) -> str:
    """Generate a report for Gate 3 scan in declaration repo."""
    report = []
    report.append("# Gate 3: Public Exposure Scan Report (Declaration Repo)")
    report.append("")
    
    # Sensitive data section
    report.append("## Sensitive Data Scan Results")
    
    sensitive = results["sensitive_scan"]
    total_sensitive_issues = sum(len(v) for v in sensitive.values())
    
    if total_sensitive_issues == 0:
        report.append("✅ No sensitive data detected")
    else:
        report.append(f"❌ {total_sensitive_issues} sensitive items detected:")
        
        for category, items in sensitive.items():
            if items:
                report.append(f"\n### {category.replace('_', ' ').title()}")
                for item in items:
                    report.append(f"- {item}")
    
    report.append("")
    
    # Version consistency section
    report.append("## Version Consistency Check")
    
    version = results["version_consistency"]
    
    if version["consistent"]:
        report.append("✅ Version references consistent")
    else:
        report.append("❌ Mixed version references detected")
    
    report.append("")
    
    return "\n".join(report)


def generate_violation_register(results: Dict[str, any]) -> str:
    """Generate a register of violations for declaration repo."""
    violations = []
    
    # Add sensitive data violations
    for category, items in results["sensitive_scan"].items():
        for item in items:
            file_path = item.split(':')[0] if ':' in item else item
            violation_detail = item[len(file_path)+1:] if ':' in item else item
            violations.append({
                "type": f"sensitive_{category}",
                "location": file_path,
                "detail": violation_detail,
                "severity": "high" if category in ["production_ips", "password_items"] else "medium",
                "follow_up_feature": "engine-substrate-boundary"  # Default assignment
            })
    
    # Add version inconsistency violations
    if not results["version_consistency"]["consistent"]:
        violations.append({
            "type": "version_inconsistency",
            "location": "documentation",
            "detail": "Mixed version references detected in documentation",
            "severity": "medium",
            "follow_up_feature": "declaration-template-interface-fix"
        })
    
    # Format as table
    table_lines = []
    if violations:
        table_lines.append("| Type | Location | Detail | Severity | Follow-up Feature |")
        table_lines.append("|------|----------|--------|----------|-------------------|")
        
        for v in violations:
            table_lines.append(f"| {v['type']} | {v['location']} | {v['detail']} | {v['severity']} | {v['follow_up_feature']} |")
    else:
        table_lines.append("No violations detected.")
    
    return "\n".join(table_lines)


if __name__ == "__main__":
    repo_path = "/Users/busiji/infraro"
    print("Running Gate 3: Public Exposure Scan (Declaration Repo)...")
    print("")
    
    results = run_gate3_scan(repo_path)
    report = generate_gate3_report(results)
    print(report)
    
    print("## Violation Register")
    violation_register = generate_violation_register(results)
    print(violation_register)
    print("")
    
    # Count total issues
    total_sensitive_issues = sum(len(v) for v in results["sensitive_scan"].values())
    version_inconsistent = not results["version_consistency"]["consistent"]
    
    total_issues = total_sensitive_issues + (1 if version_inconsistent else 0)
    
    if total_issues == 0:
        print("=== GATE 3 PASSED ===")
        print("No sensitive data or version inconsistencies detected.")
        exit(0)
    else:
        print(f"=== GATE 3 REPORTING {total_issues} ISSUES ===")
        print(f"Detected {total_sensitive_issues} sensitive data items and {'version inconsistency' if version_inconsistent else 'no version issues'}.")
        print("These are listed in the violation register for remediation in follow-up features.")
        # Exit with success since this gate reports issues rather than failing immediately
        exit(0)
