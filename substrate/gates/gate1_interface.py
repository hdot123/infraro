"""Gate 1: Interface Reality (declaration repo).

Every declaration template's engine call must match the engine's declared
face, per key:

1. ``uses: hdot123/infraro-core-mirror/.github/workflows/X.yml@<ref>`` — the
   workflow must exist and the call's ``with:``/``secrets:`` keys must match
   its ``workflow_call`` face exactly (undeclared key passed → red; required
   key missing → red). ``<ref>`` must be a live tag on the engine remote
   (dead-tag detection, e.g. the @v0.15.0 class).
2. ``uses: hdot123/infraro-core-mirror/actions/<name>@<sha-or-tag>`` — the composite action
   must exist, input keys must match its face, and the pinned SHA must exist
   in engine history.
3. Declaration docs referencing engine workflows/actions must use live refs.

Engine face source: ``ENGINE_REPO_DIR`` (CI cross-repo checkout) or the local
sibling ``../infraro-core-mirror``. Ref/SHA existence: engine clone when available,
else ``git ls-remote`` (anonymous, public repo). Stock findings already in
substrate/gate0-exemptions.md (owner + owning feature) are reported but do
not fail; NEW findings do.

M6.2 bridge: the gates validate the mirror face (what templates anchor).
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

from gate_common import (
    ENGINE_REPO_SLUG,
    REPO_ROOT,
    action_face,
    engine_dir,
    finish,
    load_yaml,
    registry_entries,
    remote_tags,
    workflow_call_face,
)

WORKFLOW_USES = re.compile(
    rf"{re.escape(ENGINE_REPO_SLUG)}/\.github/workflows/([A-Za-z0-9_.-]+\.yml)@(\S+)"
)
ACTION_USES = re.compile(
    rf"{re.escape(ENGINE_REPO_SLUG)}/actions/([A-Za-z0-9_-]+)@([0-9a-f]{{40}})"
)
DOC_REF = re.compile(
    rf"{re.escape(ENGINE_REPO_SLUG)}/(?:\.github/workflows/([A-Za-z0-9_.-]+\.yml)"
    rf"|actions/([A-Za-z0-9_-]+))@([\w.-]+)"
)


def _call_maps(doc: dict) -> list[dict]:
    """Engine-call entries: job-level reusable-workflow calls + step calls."""
    calls: list[dict] = []
    for job in (doc.get("jobs") or {}).values():
        if not isinstance(job, dict):
            continue
        if job.get("uses"):
            calls.append(job)
        for step in job.get("steps") or []:
            if isinstance(step, dict) and step.get("uses"):
                calls.append(step)
    return calls


def _face(engine: Path, kind: str, name: str) -> dict | None:
    try:
        if kind == "workflow":
            return workflow_call_face(engine, name)
        return action_face(engine, name)
    except Exception:  # noqa: BLE001 - face absence is a finding, not a crash
        return None


def _sha_exists_on_remote(sha: str) -> bool | None:
    """Commit existence via GitHub API (works from shallow CI checkouts)."""
    gh = None
    for candidate in ("gh", "/usr/bin/gh", "/usr/local/bin/gh"):
        try:
            if subprocess.run([candidate, "--version"], capture_output=True, check=False).returncode == 0:
                gh = candidate
                break
        except OSError:
            continue
    if gh is None:
        return None
    proc = subprocess.run(
        [gh, "api", f"repos/{ENGINE_REPO_SLUG}/commits/{sha}"],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode == 0:
        return True
    return False if "404" in proc.stderr else None


def _ref_exists(engine: Path | None, ref: str) -> bool | None:
    """True/False when verifiable, None when no evidence source reachable."""
    is_sha = bool(re.fullmatch(r"[0-9a-f]{40}", ref))
    if engine is not None:
        probe_ref = ref + "^{commit}" if is_sha else ref
        probe = subprocess.run(
            ["git", "-C", str(engine), "rev-parse", "--verify", "--quiet", probe_ref],
            capture_output=True,
            check=False,
        )
        if probe.returncode == 0:
            return True
        # shallow/CI checkouts may lack the object; fall through to the remote
    if is_sha:
        return _sha_exists_on_remote(ref)
    repo_url = f"https://github.com/{ENGINE_REPO_SLUG}"
    tags = remote_tags(repo_url)
    return (ref in tags) if tags else None


def check_template_calls(
    engine: Path | None, tags_cache: dict[str, bool | None]
) -> tuple[list[str], list[str]]:
    """Per-key validation of every template's engine calls."""
    errors: list[str] = []
    templates_dir = REPO_ROOT / "templates"
    for template_path in sorted(templates_dir.glob("*.yml")):
        doc = load_yaml(template_path)
        if not isinstance(doc, dict):
            continue
        for step in _call_maps(doc):
            uses = str(step.get("uses", ""))
            wf = WORKFLOW_USES.match(uses)
            act = ACTION_USES.match(uses)
            if not wf and not act:
                if uses.startswith(ENGINE_REPO_SLUG):
                    errors.append(
                        f"{template_path.name}: engine uses without a 40-hex SHA or tag ref: {uses}"
                    )
                continue
            if wf:
                name, ref = wf.group(1), wf.group(2)
                face = _face(engine, "workflow", name) if engine else None
                if face is None:
                    errors.append(
                        f"{template_path.name}: engine workflow face unreadable for {name}"
                    )
                    continue
                declared_inputs = set(face["inputs"])
                declared_secrets = set(face["secrets"])
            else:
                name, ref = act.group(1), act.group(2)
                face = _face(engine, "action", name) if engine else None
                if face is None:
                    errors.append(
                        f"{template_path.name}: engine action face unreadable for {name}"
                    )
                    continue
                declared_inputs = set(face["inputs"])
                declared_secrets = set()
            passed_inputs = set(step.get("with") or {})
            passed_secrets = set(step.get("secrets") or {})
            for key in sorted(passed_inputs - declared_inputs):
                errors.append(
                    f"{template_path.name}: passes UNDECLARED input '{key}' to {name}"
                )
            for key in sorted(passed_secrets - declared_secrets):
                errors.append(
                    f"{template_path.name}: passes UNDECLARED secret '{key}' to {name}"
                )
            required_inputs = {
                k for k, v in face["inputs"].items() if isinstance(v, dict) and v.get("required")
            }
            for key in sorted(required_inputs - passed_inputs):
                errors.append(
                    f"{template_path.name}: missing REQUIRED input '{key}' for {name}"
                )
            required_secrets = {
                k for k, v in face.get("secrets", {}).items()
                if isinstance(v, dict) and v.get("required")
            }
            for key in sorted(required_secrets - passed_secrets):
                errors.append(
                    f"{template_path.name}: missing REQUIRED secret '{key}' for {name}"
                )
            if ref not in tags_cache:
                tags_cache[ref] = _ref_exists(engine, ref)
            if tags_cache[ref] is False:
                errors.append(f"{template_path.name}: DEAD ref {ref} for {name}")
            elif tags_cache[ref] is None:
                errors.append(f"{template_path.name}: ref {ref} for {name} UNVERIFIED (no evidence source)")
    return errors


def check_docs_refs(tags_cache: dict[str, bool | None]) -> list[str]:
    errors: list[str] = []
    docs_dirs = [REPO_ROOT / "docs", REPO_ROOT / "project-map"]
    docs_files = [p for d in docs_dirs if d.is_dir() for p in sorted(d.rglob("*.md"))]
    docs_files += [p for p in (REPO_ROOT / "README.md", REPO_ROOT / "INDEX.md") if p.exists()]
    for md in docs_files:
        for wf_name, act_name, ref in DOC_REF.findall(
            md.read_text(encoding="utf-8", errors="replace")
        ):
            name = wf_name or act_name
            if ref not in tags_cache:
                tags_cache[ref] = _ref_exists(engine_dir(), ref)
            if tags_cache[ref] is False:
                errors.append(f"{md.relative_to(REPO_ROOT)}: DEAD engine ref {name}@{ref}")
    return errors


def main() -> int:
    engine = engine_dir()
    tags_cache: dict[str, bool | None] = {}
    findings = check_template_calls(engine, tags_cache)
    findings += check_docs_refs(tags_cache)
    if engine is None:
        findings.append(
            "engine face source unavailable (set ENGINE_REPO_DIR; CI injects the "
            "cross-repo checkout)"
        )
    registered = registry_entries("Gate 1")
    red, stock = [], []
    for err in findings:
        (stock if any(tok in err for tok in registered) else red).append(err)
    return finish(
        "Gate 1: Interface Reality (declaration repo)", red, stock,
        [f"engine face source: {engine or 'UNAVAILABLE'}"],
    )


if __name__ == "__main__":
    raise SystemExit(main())
