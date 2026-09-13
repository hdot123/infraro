# Consumer Onboarding Guide (v3)

This guide explains how to integrate your repository with the infraro infrastructure automation engine using the new v3 anonymous access model.

## Prerequisites

- GitHub repository (public or private)
- Appropriate permissions to add workflows and secrets
- Self-hosted runner (for private repositories) or GitHub-hosted runners

## Installation

Use the anonymous installation method (no ORG_READ_TOKEN or engine_read_token required):

```bash
# The infraro engine is accessible via anonymous git+https
pip install git+https://github.com/hdot123/infraro-core.git@v0.18.4
```

## Workflow Templates

Choose the appropriate workflow template for your use case:

- [Scan](../templates/scan.yml) - Security and compliance scanning
- [Heartbeat](../templates/heartbeat.yml) - Regular repository health checks  
- [Governance](../templates/governance.yml) - Policy enforcement and governance
- [Branch Cleanup](../templates/branch-cleanup.yml) - Automated branch cleanup
- [Auto Merge](../templates/auto-merge.yml) - Automatic pull request merging
- [Droid Review](../templates/droid-review.yml) - Automated code review
- [Watchdog](../templates/watchdog.yml) - Monitoring and alerting

## Per-Repository Runner Registration

For private repositories, register a per-repository runner on your self-hosted machine:

```bash
# Register a runner for your specific repository
./config.sh --url https://github.com/<OWNER>/<REPO_NAME> --token <RUNNER_TOKEN>

# The runner should use the following labels:
# self-hosted, pve-linux
```

## Configuration

Add the following secrets to your repository:

- `DISPATCH_TOKEN`: GitHub personal access token with appropriate permissions

## Naming Convention

All infraro-related workflows follow standardized naming:

- CI workflows: `CI`
- OK status indicators: `ci-ok`, `qa-ok` 
- Gate workflows: `gate/*`

## Security & Compliance

- All workflows use GitHub's security features (dependency review, secret scanning)
- Workflows are pinned to specific versions using tagged releases
- No hardcoded credentials in templates

## Support

For support, please check the [infraro documentation](../README.md) or open an issue in the [infraro-core repository](https://github.com/hdot123/infraro-core).
