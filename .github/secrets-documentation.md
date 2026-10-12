# Required Secrets for Declaration Repository

The following secrets need to be configured in the GitHub repository settings for the workflows to function properly:

## Droid Review Secrets
- `FACTORY_API_KEY`: API key for Factory Droid access
- `OPENCODE_GO_KEY`: OpenCode Go subscription key (BYOM Authorization passthrough)  
- `GO_GITHUB_RUN_TOKEN`: Cloudflare AI Gateway run token (cf-aig-authorization)

## Auto Merge Secrets
- `DISPATCH_TOKEN`: Personal Access Token with permissions to merge PRs

## Branch Cleanup Secrets
- `dispatch_token`: Personal Access Token for branch cleanup operations (same as DISPATCH_TOKEN but with different naming convention for the action)
- `linear_api_key`: API key for Linear integration (if used)

These secrets are required for the thin-caller workflows to function correctly.

## Repo Variables vs Secrets（vars 值会进 run 日志）

GitHub prints repo variable values into run logs as-is — variables are **not masked** (masking is a secrets-only behavior). 规则（与入口说明及交付标准一致）：repo variable 值会原样打印进 run 日志（不被打码），公开仓的 webhook/回调 URL 必须走 secret，vars 形态仅限私有仓。

Consequences for this repository (public) and all consumer repos:

- Never configure a webhook/callback URL as a repo variable in a **public** repo — the URL would be exposed verbatim in public run logs and become an enumerable attack surface, even though a URL is usually considered configuration rather than a credential. Use a secret instead.
- `vars:` injection is only acceptable in **private** repos, where run logs are not publicly readable.
