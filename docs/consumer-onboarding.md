# Consumer Onboarding Guide (v3)

This guide explains how to set up a consumer repository to work with the infraro engine system using the v3 architecture.

## Architecture Overview

The v3 architecture uses public engine repositories with anonymous access:

- **Public engine**: `hdot123/infraro-core` (public, anonymous access)
- **Declaration layer**: `hdot123/infraro` (public, contains templates and docs)
- **Consumer repositories**: Private repositories that consume the engine

## Installation

The engine can be installed anonymously without requiring any private tokens:

```bash
# Install the engine using git+https (no token required)
pip install git+https://github.com/hdot123/infraro-core.git@v0.18.4
```

**Note**: This is a public repository that can be accessed anonymously. No ORG_READ_TOKEN, engine_read_token, or 1Password credentials are required.

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

Use the provided workflow templates from the declaration repository. All templates use the `uses@tag` anchor discipline (full anchor with engine=workflow=same tag), prohibiting `@main` usage.

Templates available:

- scan.yml
- heartbeat.yml
- governance.yml
- branch-cleanup.yml
- auto-merge.yml
- droid-review.yml
- watchdog.yml

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

- [Template Directory](../templates/)
- [Naming Contracts](../docs/naming-contracts.md)
- [Base Layer Templates](../docs/base-layer-templates.md)
- [Double True Source Declaration](../docs/double-true-source.md)
- [Boundary Documentation](../docs/BOUNDARY.md)
