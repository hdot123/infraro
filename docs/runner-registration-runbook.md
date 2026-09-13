# Per-Repository Runner Registration Runbook

This runbook provides instructions for registering self-hosted runners for individual repositories that use infraro.

## Requirements

- Access to self-hosted runner machine (recommended: Linux with pve-linux environment)
- GitHub personal access token with repo permissions
- Repository admin access

## Registration Process

1. On your self-hosted machine, navigate to your Actions Runner directory
1. Run the configuration command:

```bash
# Register a runner for a specific repository
./config.sh --url https://github.com/<OWNER>/<REPO_NAME> --token <RUNNER_REGISTRATION_TOKEN>
```

1. Ensure the runner uses the correct labels:

```text
self-hosted
pve-linux
```

## Labels Explanation

- `self-hosted`: Identifies this as a self-hosted runner (not GitHub-hosted)
- `pve-linux`: Specifies the environment type for infraro workflows

## Verification

After registration, verify that:

1. The runner appears in the repository's Settings → Actions → Runners
1. The runner shows as "Online"
1. Workflows can successfully use the runner

## Maintenance

- Monitor runner logs regularly
- Update runner software as needed
- Verify that labels remain consistent
- Ensure network connectivity to GitHub

## Troubleshooting

If a runner goes offline:
1. Check network connectivity
1. Verify the runner process is running
1. Review runner logs for errors
1. Re-register if necessary
