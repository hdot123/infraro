# Per-Repository Baseline Templates

This document outlines the recommended baseline configuration for repositories integrating with infraro.

## Ruleset要点

Recommended rules for all infraro-enabled repositories:

- Require pull request before merging
- Require approvals (typically 1 or more)
- Require status checks to pass before merging
- Require branches to be up to date before merging
- Prevent force pushes to matching branches
- Prevent deletion of matching branches

## Allowlist

Recommended allowed actions for security:

- `hdot123/infraro-core/**` - infraro engine workflows
- `actions/*` - GitHub official actions
- `github/*` - GitHub specific actions
- Selected third-party actions as needed

## Secrets

Required secrets for infraro functionality:

- `DISPATCH_TOKEN` - GitHub personal access token with appropriate permissions

## Squash-Only

Configuration for squash-only merging:

- Enable "Always suggest updating pull request branch"
- Enable "Allow squash merging"
- Disable "Allow merge commits"
- Disable "Allow rebase merging"
- Enable "Automatically delete head branches"
