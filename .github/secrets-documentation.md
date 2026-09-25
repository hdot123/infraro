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
