"""Gate 0: Coverage Completeness (declaration repo).

Enumerates every tracked top-level path/asset and checks each against the
declared checker scan domains (markdownlint, actionlint, gate1 templates,
gate3 repo-wide exposure scan, this suite). Unowned areas must appear in the
substrate/gate0-exemptions.md Gate 0 registry (exemption = registration +
owner) or the gate fails.

Scan-domain inventory (declaration repo):
=======================  ====================================================
templates/               gate1 interface reality (engine call faces + refs)
docs/                    markdownlint + gate3 exposure scan
project-map/             markdownlint + gate3 exposure scan
substrate/               substrate gate suite (this suite's own domain)
.github/                 actionlint (workflow files)
tests/                   markdownlint (.memory-anchor.md); py stubs retired
tools/, scripts/         gate3 exposure scan ONLY (registered: no dedicated
                         linter wired in declaration CI yet)
AGENTS.md/README.md/     markdownlint + gate3 exposure scan
INDEX.md/NOW.md
.markdownlint.json       markdownlint's own config
.gitignore               git hygiene (own tool)
LICENSE                  REGISTERED exemption (static legal text)
=======================  ====================================================
"""

from __future__ import annotations

import subprocess

from gate_common import REGISTRY_PATH, REPO_ROOT, registry_entries

# Entries fully inside a checker's scan domain (see module docstring).
COVERED_ENTRIES = frozenset(
    {
        ".github",
        ".gitignore",
        ".markdownlint.json",
        "AGENTS.md",
        "INDEX.md",
        "NOW.md",
        "README.md",
        "docs",
        "project-map",
        "substrate",
        "templates",
        "tests",
    }
)


def top_level_entries() -> set[str]:
    out = subprocess.run(
        ["git", "ls-files"], cwd=REPO_ROOT, capture_output=True, text=True, check=True
    )
    entries: set[str] = set()
    for line in out.stdout.splitlines():
        entries.add(line.split("/", 1)[0])
    return entries


def main() -> int:
    entries = top_level_entries()
    unowned = sorted(e for e in entries if e.rstrip("/") not in COVERED_ENTRIES)
    registered = set(registry_entries("Gate 0"))
    missing = [e for e in unowned if e not in registered]

    print("# Gate 0: Coverage Completeness (declaration repo)")
    print(f"- tracked top-level entries: {len(entries)}")
    print(f"- inside a checker scan domain: {len(entries) - len(unowned)}")
    print(f"- unowned: {len(unowned)} (registered: {len(unowned) - len(missing)})")
    for entry in unowned:
        state = "registered" if entry in registered else "UNREGISTERED"
        print(f"  - {entry} [{state}]")
    print(f"- registry: {REGISTRY_PATH}")
    red = [
        f"{e} unowned and missing from the Gate 0 registry (owner + feature)"
        for e in missing
    ]
    if red:
        print(
            "FAIL: unowned entries missing from the Gate 0 registry (owner + feature):"
        )
        for item in red:
            print(f"  - {item}")
        return 1
    print(
        "PASS: every top-level entry is covered or registered "
        "(exemption = registration + owner)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
