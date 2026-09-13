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

## 引擎转私 runner 迁移清单

### 触发条件
- infraro-core 转为私有仓

### 动作清单
1. **工作流文件替换**：将引擎仓内所有 workflows 的 `runs-on` 从 `ubuntu-latest` 逐文件替换为 `self-hosted,pve-linux`
   - 位置：`.github/workflows/` 目录下的所有 YAML 文件
   - 搜索：`runs-on: ubuntu-latest`
   - 替换：`runs-on: [self-hosted, pve-linux]`

2. **pve runner 在册核验**：
   - 登录 ce-01 服务器
   - 检查 `/home/runner/` 目录下的 Actions Runner 目录
   - 确认 infraro-core 仓库的 runner 服务正在运行
   - 运行 `systemctl status actions-runner-<repo-name>` 检查服务状态

3. **回滚说明**：
   - 如需回滚，将 `runs-on` 配置改回 `ubuntu-latest`
   - 在私有仓中，self-hosted runners 可以更好地控制环境和资源

### 理由
- **私仓无可信性问题**：私有仓库的代码和工作流是可控的，使用 self-hosted runners 更安全
- **免烧 GitHub Pro 分钟数**：私有仓库使用 GitHub-hosted runners 需要付费分钟数，self-hosted runners are unlimited

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
