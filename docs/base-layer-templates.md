# Per-Repository Base Layer Templates

This document provides templates for the baseline configuration that should be applied to each repository in the infraro ecosystem.

## Branch Protection Ruleset

Apply these rules to protect your main branch:

- Require pull request before merging
- Require status checks before merging (e.g., `ci-ok`)
- Require branches to be up to date before merging
- Restrict who can dismiss pull request reviews
- Restrict pushes that can bypass pull requests

## Actions Allowlist

Configure GitHub Actions permissions:

- Set `allowed_actions` to `selected`
- Add patterns for trusted actions:
  - `hdot123/infraro-core/**`
  - `actions/*`
  - `github/*`
  - Other trusted third-party actions

## Secrets Configuration

Recommended secrets for consumer repositories:

- `DISPATCH_TOKEN`: Fine-grained personal access token for automation
- Other service-specific tokens as needed

## Merge Settings

Configure repository merge settings:

- Enable `Allow squash merging`
- Disable `Allow merge commits`
- Disable `Allow rebase merging`
- Enable `Automatically delete head branches`

## Required Checks

Configure these required status checks:

- `ci-ok` - Continuous integration success
- `Droid Auto Review` - Code review completion
- Other quality gates as appropriate
