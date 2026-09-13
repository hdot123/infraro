"""Shared helpers for the declaration-repo substrate gates (门0-门4).

Public-repo hygiene: no gate script ever hardcodes a host path (zero
``/Users/``, zero ``/home/``). The engine repo is resolved via
``ENGINE_REPO_DIR`` (CI injects it from a cross-repo checkout); locally the
default sibling checkout ``../infraro-core`` is used when present.

Stock matching: gate findings that reproduce previously-registered stock are
reported (never silently dropped) and do not fail the run, provided the
registry entry carries an owner and an owning feature. NEW findings fail.
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
ENGINE_REPO_URL = "https://github.com/hdot123/infraro-core"
ENGINE_REPO_SLUG = "hdot123/infraro-core"
REGISTRY_PATH = REPO_ROOT / "substrate" / "gate0-exemptions.md"


def engine_dir() -> Path | None:
    """Locate an engine checkout: env override, then the default sibling."""
    env_dir = os.environ.get("ENGINE_REPO_DIR")
    if env_dir:
        candidate = Path(env_dir)
        if (candidate / ".github" / "workflows").is_dir():
            return candidate
    sibling = REPO_ROOT.parent / "infraro-core"
    if (sibling / ".github" / "workflows").is_dir():
        return sibling
    return None


def remote_tags(repo_url: str) -> set[str]:
    """All tag names on the remote (anonymous; public repo)."""
    proc = subprocess.run(
        ["git", "ls-remote", "--tags", repo_url],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return set()
    tags: set[str] = set()
    for line in proc.stdout.splitlines():
        ref = line.split("\t", 1)[1] if "\t" in line else ""
        ref = ref.removeprefix("refs/tags/")
        if ref and not ref.endswith("^{}"):
            tags.add(ref)
    return tags


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def workflow_call_face(engine: Path, workflow_name: str) -> dict[str, Any]:
    """The ``on.workflow_call`` face of an engine workflow (inputs/secrets)."""
    path = engine / ".github" / "workflows" / workflow_name
    doc = load_yaml(path)
    on = doc.get("on") if isinstance(doc, dict) else None
    if on is None and isinstance(doc, dict):  # YAML 1.1: bare `on` parses as True
        on = doc.get(True)
    call = (on or {}).get("workflow_call") if isinstance(on, dict) else None
    call = call or {}
    return {
        "inputs": call.get("inputs") or {},
        "secrets": call.get("secrets") or {},
    }


def action_face(engine: Path, action_name: str) -> dict[str, Any]:
    """The inputs face of an engine composite action."""
    path = engine / "actions" / action_name / "action.yml"
    doc = load_yaml(path)
    return {"inputs": doc.get("inputs") or {}}


def registry_entries(section_header: str) -> list[str]:
    """First-column tokens from a registry section (owner-bearing rows only).

    Each row is ``| `token` | ... | owner | feature | ... |``; the leading
    backticked first cell is the match token for stock comparison.
    """
    if not REGISTRY_PATH.exists():
        return []
    lines = REGISTRY_PATH.read_text(encoding="utf-8").splitlines()
    entries: list[str] = []
    in_section = False
    for line in lines:
        if line.startswith("## "):
            in_section = line[3:].lstrip().startswith(section_header)
            continue
        if not in_section or not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4 or set(cells[0]) <= {"-", ":", " "}:
            continue
        token = cells[0].strip("`").strip()
        if token and cells[2] not in {"", "-"}:  # owner cell must be present
            entries.append(token)
    return entries


def tracked_files() -> list[Path]:
    out = subprocess.run(
        ["git", "ls-files"], cwd=REPO_ROOT, capture_output=True, text=True, check=True
    )
    return [REPO_ROOT / line for line in out.stdout.splitlines() if line]


def finish(name: str, red: list[str], registered: list[str], notes: list[str]) -> int:
    """Uniform honest output: report red + registered stock + notes."""
    print(f"# {name}")
    for item in red:
        print(f"- NEW FINDING: {item}")
    for item in registered:
        print(f"- REGISTERED STOCK: {item}")
    for item in notes:
        print(f"- NOTE: {item}")
    print(f"- new findings: {len(red)}; registered stock: {len(registered)}")
    if red:
        print(
            "FAIL: new findings must be fixed or registered "
            "(substrate/gate0-exemptions.md: owner + owning feature)"
        )
        return 1
    print("PASS: no new findings; existing stock registered and owned")
    return 0
