# Gate 0 Exemption Registration List

This document tracks areas identified by Gate 0 (Coverage Completeness) as requiring exemption from standard scanning domains. Each entry represents a conscious decision that the area doesn't need standard checks, with assigned ownership.

## Current Exemptions

| Path | Reason for Exemption | Owner | Follow-up Feature | Status |
|------|---------------------|-------|-------------------|--------|
| `cf/` | Cloudflare Worker infrastructure, exempted area per substrate requirements | hdot123 | engine-substrate-boundary | Registered |
| `webhook-scripts/` | Webhook handler scripts, exempted area per substrate requirements | hdot123 | engine-substrate-boundary | Registered |
| `memory/` | Private memory system files, intentionally excluded from public repo | hdot123 | - | Excluded |
| `tests/` | Test files directory - requires custom scanning approach | hdot123 | engine-substrate-boundary | Registered |
| `project-map/` | Project mapping configuration files | hdot123 | engine-substrate-boundary | Registered |
| `.git/` | Git metadata directory - not scanned by conventional tools | hdot123 | engine-substrate-boundary | Registered |
| `tools/` | Tool configuration and utilities | hdot123 | engine-substrate-boundary | Registered |
| `.DS_Store` | macOS system file | hdot123 | engine-substrate-boundary | Registered |
| `.venv/` | Python virtual environment (engine repo) | hdot123 | engine-substrate-boundary | Registered |
| `scripts/` | Script files (engine repo) - needs separate validation | hdot123 | engine-substrate-boundary | Registered |
| `test_shell_guards.sh` | Shell guard testing utility (engine repo) | hdot123 | engine-substrate-boundary | Registered |
| `.pytest_cache/` | Pytest cache directory (engine repo) | hdot123 | engine-substrate-boundary | Registered |
| `actions/` | GitHub Actions composite actions directory (engine repo) | hdot123 | engine-substrate-boundary | Registered |
| `.ruff_cache/` | Ruff cache directory (engine repo) | hdot123 | engine-substrate-boundary | Registered |
| `.evolution/` | Evolution framework configuration (engine repo) | hdot123 | engine-substrate-boundary | Registered |
| `docs/` | Documentation directory - may need custom validation (engine repo) | hdot123 | engine-substrate-boundary | Registered |
| `.mypy_cache/` | MyPy cache directory (engine repo) | hdot123 | engine-substrate-boundary | Registered |

## Process

When Gate 0 identifies an unowned area, it should be evaluated:
1. Is it truly unowned or does it need to be covered by a specific check?
2. If intentionally exempt, register it in this list with owner assignment
3. If it should be covered, implement the appropriate check

## Gate 0 Scan Results

Last run: [Automatically updated by gate test]
- Total top-level paths: [varies by repo]
- Covered paths: [varies by repo]  
- Unowned paths: [as registered above]

This ensures transparency about what's intentionally exempted vs. what needs coverage.
