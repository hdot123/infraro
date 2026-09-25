# Consumer Onboarding Guide (v3)

This guide explains how to set up a consumer repository to work with the infraro engine system using the v3 architecture.

## Architecture Overview

The v3 architecture uses a public mirror bridge for engine access (M6.2):

- **Engine logic truth source**: `hdot123/infraro-core` (source of truth for engine logic)
- **Public consumption mirror**: `hdot123/infraro-core-mirror` (public, anonymous access; mechanical release snapshots)
- **Declaration layer**: `hdot123/infraro` (public, contains templates and docs)
- **Consumer repositories**: Private repositories that consume the engine via the mirror

## Installation

The engine can be installed anonymously from the public mirror without requiring any private tokens:

```bash
# Install the engine from the public mirror via git+https (no token required)
pip install git+https://github.com/hdot123/infraro-core-mirror.git@v0.18.9
```

**Note**: The mirror is a public repository that can be accessed anonymously. Engine logic truth remains in the source engine repository; the mirror carries mechanical release snapshots. No legacy tokens or credential rotation tools are required.

## Runner Registration

For self-hosted runner registration, use the per-repository format:

```bash
# Register runner for your specific repository
./config.sh --url https://github.com/hdot123/your-repo-name --token <RUNNER_TOKEN>
```

The runner should use the following labels:

- `self-hosted`
- `pve-linux`

## Workflow Templates

Use the provided workflow templates from the declaration repository. The system uses a dual-stack approach:

- **5 thin-caller templates** (workflow-level tag anchors): evolution-scan.yml, evolution-heartbeat.yml, auto-merge.yml, droid-review.yml, droid-review-watchdog.yml - these use the `uses@tag` anchor discipline (full anchor with engine=workflow=same tag), prohibiting `@main` usage.
- **2 copy-form templates** (provenance header + composite action SHA pins): governance.yml, branch-cleanup.yml - these contain full workflow content with provenance headers and pinned composite actions at specific commit SHAs.

All templates prohibit `@main` usage in their respective anchor disciplines.

**Filename contracts** (r38 consumer-template-reconciliation): the scanner and heartbeat thin-caller filenames are load-bearing — the heartbeat engine probes scanner liveness and performs self-heal dispatch by the exact filename `evolution-scan.yml` (`gh run list --workflow` / `gh workflow run`), and the scanner reverse-watches `evolution-heartbeat.yml` (INFRA-588). Consumer repos must keep these filenames byte-exact; the watchdog caller must be named `droid-review-watchdog.yml` with workflow name `Droid Review Watchdog` so its `workflow_run` filters ("Droid Auto Review", "CI") match sibling workflows' names.

The templates are organized in a dual-stack manner:

- **Python Stack**: Located in [templates/python/](../templates/python/)
- **TypeScript Stack**: Located in [templates/typescript/](../templates/typescript/)

Both stacks contain the same 7 templates:

- evolution-scan.yml (thin-caller)
- evolution-heartbeat.yml (thin-caller)
- governance.yml (copy-form)
- branch-cleanup.yml (copy-form)
- auto-merge.yml (thin-caller)
- droid-review.yml (thin-caller)
- droid-review-watchdog.yml (thin-caller)

## Naming Contracts

The system follows fixed naming contracts that are cross-stack stable:

- Workflow name: `CI`
- Job key: `ci-ok`
- Job key: `qa-ok`
- Gate prefixes: `gate/*`

## Secrets Configuration

Use snake-only single形态 for secrets (v2-F2 birth-to-terminal state):

✅ Correct:

```yaml
secrets:
  dispatch_token: ${{ secrets.DISPATCH_TOKEN }}
```

❌ Incorrect:

```yaml
secrets:
  DISPATCH-TOKEN: ${{ secrets.DISPATCH_TOKEN }}  # Do not use hyphens
```

## Base Layer Template

Follow the per-repository base template for repository settings:

- Branch protection ruleset
- Actions allowlist
- Secrets setup
- Squash-only merge settings

## Engine Authorization Preflight（三态与申请入口）

Engine consumption is allowlist-gated. The single source of truth for who may consume the engine is
[`hdot123/scheduler` → `authorized.yaml`](https://github.com/hdot123/scheduler/blob/main/authorized.yaml)
(唯一登记与对账入口；不构成匿名拉取的技术闸门；技术强制需凭证链／已列为不迁移项的除外)。
Before wiring any engine workflows into a repo, check which preflight state the repo is in
(full copy spec: [Preflight Status Spec](preflight-status.md)):

- **待申请 (pending application, neutral guidance)** — repo not in the allowlist and no channel legs yet.
  Apply at the entry point: open a PR adding the repo name to the `authorized` list in
  [`authorized.yaml`](https://github.com/hdot123/scheduler/blob/main/authorized.yaml).
  After merge, the scheduler repo's `whitelist-sync` workflow (plan → apply) lays down the channel legs.
- **权限故障 (credential fault, red → owner)** — authorization unreadable / PAT unreachable.
  This is a scheduler-side credential problem (PAT scope, expiry, or revocation); consumers cannot self-heal.
  Escalate to the owner of the scheduler repo (1Password `GitHub-PAT-A-Z` custodian).
- **已授权缺配 (authorized but unsynced, red → sync)** — repo listed in `authorized.yaml` but legs missing
  (variable / secret / runner). Check the scheduler repo's pinned issue「白名单对账 · 每日状态」for the
  🟡 row, then run scheduler's `whitelist-sync` workflow: `mode=plan` to get the plan and `plan_hash`,
  then `mode=apply` with that hash.

Standard fail-closed copy seen at pipeline entry when unauthorized:

> 未授权消费引擎，走授权流程：本仓未设置 repo variable `ENGINE_CONSUMERS`
> （授权四步：variable → PAT → runner → 6 阶段验收）。
> 申请入口：向 [hdot123/scheduler 的 authorized.yaml](https://github.com/hdot123/scheduler/blob/main/authorized.yaml)
> 提 PR 加一行本仓名，合并后由 whitelist-sync 铺设通道。

## Double True Source Declaration

- `hdot123/infraro-core` = Engine unique forward original source
- `hdot123-org/infra-core` = Frozen maintenance, backward compatibility

The following capabilities are not migratable:

- Internal proxy packages
- Forwarding packages
- Legacy internal gateways

## Boundary and Architecture Map

### v3 Architecture Layers:

1. `hdot123` (personal account)
   - `infraro-core` (public engine)
   - `infraro` (public declaration layer)
2. `hdot123/consumer-a` (private consumer repo)
3. Old world frozen repositories (for backward compatibility)

### Denial Items Archive:

- Proxy packages (denied)
- Forwarding packages (denied)
- Internal gateways (denied)

## Additional Resources

- [Python Stack Templates](../templates/python/)
- [TypeScript Stack Templates](../templates/typescript/)
- [Naming Contracts](../docs/naming-contracts.md)
- [Base Layer Templates](../docs/base-layer-templates.md)
- [Preflight Status Spec](../docs/preflight-status.md)
- [Double True Source Declaration](../docs/double-true-source.md)
- [Boundary Documentation](../docs/BOUNDARY.md)
