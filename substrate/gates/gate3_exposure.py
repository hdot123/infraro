"""Gate 3: Public Exposure Scan (declaration repo).

Repo-wide sensitive scan over tracked files: production IPs, host-local
paths (/Users/, /home/), personal emails, runner-topology hostnames, and
1Password item references. The declaration repo's docs/templates carry
machine-facing content, so the only tolerances are: RFC 5737 documentation
IPs, @users.noreply.github.com/example emails, and GitHub-hosted runner
homes. Version four-source consistency is engine-owned (the declaration repo
has no pyproject/manifest/__init__ version sources) and intentionally not
duplicated here.

This file's own regex literals reference /Users/ and /home/ as scan
patterns; scanner self-references under substrate/gates/ are excluded and
registered in substrate/gate0-exemptions.md (Gate 3 self-exclusion row).
"""

from __future__ import annotations

import re

from gate_common import REPO_ROOT, finish, registry_entries, tracked_files

IP_RE = re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b")
LOCAL_PATH_RE = re.compile(r"(?P<path>/Users/[A-Za-z0-9_.-]+|/home/[A-Za-z0-9_.-]+)")
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
RUNNER_RE = re.compile(r"\b(?:runner|actions-runner)[.-]?(?:node|host|pool)?-?\d*\b", re.IGNORECASE)
# Exposure form = a machine-resolvable item reference (op://vault/item).
# Bare prose mentions of the product name reveal nothing and are accepted.
ONEPASSWORD_RE = re.compile(r"\bop://[A-Za-z0-9_.-]+/[^\s\"'|]+")

DOC_IPS = {"192.0.2.", "198.51.100.", "203.0.113."}
EMAIL_ACCEPTS = re.compile(r"@(users\.)?noreply\.(github|example)\.com$|@example\.(com|org)$")
RUNNER_HOSTS = {"runner", "actions-runner"}
# Scanner self-references: the gate suite's own pattern literals live under
# substrate/gates/ and are excluded wholesale (registered in the registry).
SELF_SCAN_PREFIX = "substrate/gates/"


def scan() -> tuple[list[str], list[str]]:
    findings: list[str] = []
    accepts: list[str] = []
    for path in tracked_files():
        rel = path.relative_to(REPO_ROOT).as_posix()
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            if rel.startswith(SELF_SCAN_PREFIX) and (
                "LOCAL_PATH_RE" in line or "/Users/" in line or "/home/" in line
            ):
                continue  # scanner self-reference (registered)
            for match in IP_RE.findall(line):
                if any(match.startswith(prefix) for prefix in DOC_IPS):
                    continue
                if re.fullmatch(r"127\.0\.0\.1|0\.0\.0\.0|255\.255\.255\.255", match):
                    continue
                findings.append(f"{rel}:{lineno} ip:{match}")
            for match in LOCAL_PATH_RE.finditer(line):
                p = match.group("path")
                if p in {"/Users/runner", "/home/runner"}:
                    accepts.append(f"{rel}:{lineno} runner-home:{p}")
                    continue
                findings.append(f"{rel}:{lineno} local-path:{p}")
            for match in EMAIL_RE.findall(line):
                if EMAIL_ACCEPTS.search(match):
                    continue
                findings.append(f"{rel}:{lineno} email:{match}")
            for match in ONEPASSWORD_RE.findall(line):
                findings.append(f"{rel}:{lineno} 1password:{match}")
            for match in RUNNER_RE.findall(line):
                host = match.lower().split(".")[0].rstrip("-0123456789")
                if host in RUNNER_HOSTS:
                    accepts.append(f"{rel}:{lineno} runner-hostname:{match}")
                    continue
                findings.append(f"{rel}:{lineno} runner-topology:{match}")
    return findings, accepts


def main() -> int:
    findings, accepts = scan()
    registered = registry_entries("Gate 3")
    red, stock = [], []
    for err in findings:
        (stock if any(tok in err for tok in registered) else red).append(err)
    notes = [
        "version four-source check: engine-owned (declaration repo has no version sources)",
    ] + [f"accepted: {a}" for a in accepts[:8]]
    return finish("Gate 3: Public Exposure Scan (declaration repo)", red, stock, notes)


if __name__ == "__main__":
    raise SystemExit(main())
