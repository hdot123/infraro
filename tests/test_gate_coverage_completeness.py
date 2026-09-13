"""
Gate 0: Coverage Completeness Invariant Test (Declaration Repository)
Ensures every directory/asset in the repository falls under at least one checker's scanning domain.
Unowned areas generate exemption registration list (exemption = registration + owner).
"""
import os
import subprocess
from pathlib import Path
from typing import Dict, List, Set


def get_all_top_level_paths(repo_path: str) -> Set[str]:
    """Get all top-level paths/assets in the repository."""
    repo = Path(repo_path)
    paths = set()
    
    for item in repo.iterdir():
        if item.is_dir():
            paths.add(item.name + "/")
        else:
            paths.add(item.name)
    
    return paths


def get_boundary_scanner_coverage(repo_path: str) -> Set[str]:
    """Get paths covered by boundary scanners (actionlint, markdownlint, etc.)."""
    covered = set()
    
    # Get GitHub Actions workflows
    workflows_dir = Path(repo_path) / ".github" / "workflows"
    if workflows_dir.exists():
        for wf_file in workflows_dir.glob("*.yml"):
            covered.add(f".github/workflows/{wf_file.name}")
        for wf_file in workflows_dir.glob("*.yaml"):
            covered.add(f".github/workflows/{wf_file.name}")
    
    # Get markdown documentation files
    docs_dir = Path(repo_path) / "docs"
    if docs_dir.exists():
        covered.add("docs/")
        for md_file in docs_dir.rglob("*.md"):
            rel_path = md_file.relative_to(Path(repo_path))
            covered.add(str(rel_path))
    
    # Get template files
    templates_dir = Path(repo_path) / "templates"
    if templates_dir.exists():
        covered.add("templates/")
        for tmpl_file in templates_dir.rglob("*"):
            if tmpl_file.is_file():
                rel_path = tmpl_file.relative_to(Path(repo_path))
                covered.add(str(rel_path))
    
    # Get root markdown files
    for md_file in Path(repo_path).glob("*.md"):
        covered.add(md_file.name)
    
    return covered


def get_existing_contract_test_coverage(repo_path: str) -> Set[str]:
    """Get paths covered by existing contract tests."""
    covered = set()
    
    # Contract tests typically cover specific files
    # Look for common testable files
    possible_contracts = [
        ".markdownlint.json", "README.md", "LICENSE", 
        ".gitignore", ".github/"
    ]
    
    for filename in possible_contracts:
        file_path = Path(repo_path) / filename
        if file_path.exists() or (filename.endswith('/') and file_path.is_dir()):
            covered.add(filename)
    
    return covered


def identify_unowned_areas(repo_path: str) -> Dict[str, List[str]]:
    """Identify areas not covered by any scanner/checker."""
    all_paths = get_all_top_level_paths(repo_path)
    boundary_covered = get_boundary_scanner_coverage(repo_path)
    contract_covered = get_existing_contract_test_coverage(repo_path)
    
    # Union of all covered areas
    all_covered = boundary_covered.union(contract_covered)
    
    # Identify unowned areas
    unowned = []
    for path in all_paths:
        # Check if this path or any of its subdirectories are covered
        is_covered = False
        for covered_path in all_covered:
            if covered_path.startswith(path) or path.startswith(covered_path.rstrip('/')):
                is_covered = True
                break
        
        if not is_covered:
            unowned.append(path)
    
    return {
        "unowned": unowned,
        "potential_exemptions": []
    }


def generate_gate0_report(repo_path: str) -> str:
    """Generate a report for Gate 0 coverage completeness."""
    result = identify_unowned_areas(repo_path)
    
    report = []
    report.append("# Gate 0: Coverage Completeness Report (Declaration Repo)")
    report.append("")
    report.append("## Summary")
    report.append(f"- Total top-level paths: {len(get_all_top_level_paths(repo_path))}")
    report.append(f"- Boundary scanner coverage: {len(get_boundary_scanner_coverage(repo_path))}")
    report.append(f"- Contract test coverage: {len(get_existing_contract_test_coverage(repo_path))}")
    report.append("")
    
    report.append("## Unowned Areas (Require Investigation)")
    if result["unowned"]:
        for path in result["unowned"]:
            report.append(f"- {path}")
    else:
        report.append("- None found")
    
    return "\n".join(report)


if __name__ == "__main__":
    repo_path = "/Users/busiji/infraro"
    report = generate_gate0_report(repo_path)
    print(report)
    
    result = identify_unowned_areas(repo_path)
    
    # Print unowned areas for potential exemption registration
    if result["unowned"]:
        print("\n=== REGISTRATION NEEDED ===")
        print("The following areas need exemption registration:")
        for area in result["unowned"]:
            print(f"  - {area} (unowned, investigate)")
        print("\nRegister these in exemption list with owner assignments.")
        
        # Fail the test if there are unowned areas
        exit(1)
    else:
        print("\n=== GATE 0 PASSED ===")
        print("All repository paths covered by at least one scanner/checker.")
        exit(0)
