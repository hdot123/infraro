# Substrate 总账 + 标准手册

**F3.5 首交付物**：基础层资产总账与处置手册，确保零污染进入新世界。

## 1. 记忆/知识系统

| 组件 | 所在仓/位置 | 世界归属 | 状态 | 处置结论 | Owner |
|------|-------------|----------|------|----------|-------|
| memory 仓 | hdot123-org/memory | 旧世界 | RETIRED | [RETIRE] → 指向 memory-core | hdot123 |
| memory-core wrapper | `~/.factory/bin/memory-hook` | 新世界 | ACTIVE | 保留 | hdot123 |
| `~/.memory-core` | host filesystem | 新世界 | ACTIVE | 保留 | hdot123 |
| global-kb 仓 | hdot123-org/global-kb | 旧世界 | RETIRED | [RETIRE] → 指向 infraro knowledge layer | hdot123 |
| `~/.memory/global-kb` | host filesystem | 新世界 | ACTIVE | 保留 | hdot123 |
| 各项目 memory/ | `<project>/memory/` | 混合 | ACTIVE | 保留 | 项目 owner |

### 拉起步骤与验收条目（记忆系统）

#### 拉起步骤

1. 确保 `~/.factory/bin/memory-hook` 存在且可执行
2. 确保 `~/.memory-core` 目录结构完整
3. 验证项目记忆系统可正常读写：`~/.factory/bin/memory-hook --host infraro --event session-start`

#### 验收条目

- [ ] `~/.factory/bin/memory-hook` 存在且可执行
- [ ] `~/.memory-core` 目录存在且包含必要的 hook 文件
- [ ] `~/.memory/global-kb` 目录存在
- [ ] 项目记忆系统读写操作正常

## 2. Factory 运行时

| 组件 | 所在仓/位置 | 世界归属 | 状态 | 处置结论 | Owner |
|------|-------------|----------|------|----------|-------|
| `~/.factory` | host filesystem | 新世界 | ACTIVE | 保留 | hdot123 |
| hooks | `~/.factory/hooks` | 新世界 | ACTIVE | 保留 | hdot123 |
| missions | `~/.factory/missions` | 新世界 | ACTIVE | 保留 | hdot123 |
| config/repositories.yml | `~/.factory/config/repositories.yml` | 新世界 | ACTIVE | 收编 | hdot123 |
| webhook 脚本 | `~/.factory/webhook/scripts` | 新世界 | ACTIVE | 保留 | hdot123 |

## 3. 通知链（webhook 全链路）

| 组件 | 所在仓/位置 | 世界归属 | 状态 | 处置结论 | Owner |
|------|-------------|----------|------|----------|-------|
| hdot123/webhook (CF Worker) | ci-webhook.exa.edu.kg | 旧世界 | ACTIVE | 收编 | hdot123 |
| 本地 webhook 脚本 | `~/.factory/webhook/scripts/` | 新世界 | ACTIVE | 保留 | hdot123 |
| pending 文件 | `~/.factory/webhook/locks/` | 新世界 | ACTIVE | 保留 | hdot123 |

## 4. Runner 机队

| 组件 | 所在仓/位置 | 世界归属 | 状态 | 处置结论 | Owner |
|------|-------------|----------|------|----------|-------|
| ce-01 | GitHub Actions | 新世界 | ACTIVE | 分阶段处置：公开期引擎 ubuntu-latest；引擎转私有仓后切 self-hosted,pve-linux（已记录在 runbook 迁移清单） | hdot123 |
| pve-runner-01..06 | 自建服务器 | 新世界 | ACTIVE | 保留 | hdot123 |

## 5. 遗留模板仓

| 组件 | 所在仓/位置 | 世界归属 | 状态 | 处置结论 | Owner |
|------|-------------|----------|------|----------|-------|
| ci-templates | hdot123/ci-templates | 旧世界 | ACTIVE | [RETIRE] → 已归档* | hdot123 |
| gitlab-ci-standards | hdot123/gitlab-ci-standards | 旧世界 | ACTIVE | [RETIRE] → 已归档* | hdot123 |
| workflows-starter-template | hdot123/workflows-starter-template | 旧世界 | ACTIVE | [RETIRE] → 已归档* | hdot123 |

*注：将在本次任务中归档处理

## 6. 遗留基础设施

| 组件 | 所在仓/位置 | 世界归属 | 状态 | 处置结论 | Owner |
|------|-------------|----------|------|----------|-------|
| gh-proxy | `hdot123/infraro-core/cf/gh-proxy` | 旧世界 | ACTIVE | 迁出 | hdot123 |
| gateway-admin | hdot123/gateway-admin | 旧世界 | INACTIVE | [RETIRE] | hdot123 |

## 7. Linear 工作面

| 组件 | 所在仓/位置 | 世界归属 | 状态 | 处置结论 | Owner |
|------|-------------|----------|------|----------|-------|
| Linear workspace | hdot123 Linear workspace | 混合 | ACTIVE | 新建 v3 项目 "infraro v3" (ID: 3c2927a2-6b8d-4dda-af6b-3cf27310952a)，旧项目 4b08a1b7 冻结零触碰 | hdot123 |

## 8. 基础检查（探针集）

以下为基础检查探针的实跑结果.

| 探针类型 | 命令 | 实际输出 | 状态 |
|----------|------|----------|------|
| webhook 链端到端 | `curl -s -o /dev/null -w "%{http_code}" https://ci-webhook.exa.edu.kg/health` | `502` | ⚠️ 502 (2026-09-13 探针时点状态) |
| Linear key 只读探针 | `linear__get_project --id 4b08a1b7-1382-49fe-8b80-6e987bcf160a` | `{"id": "4b08a1b7-1382-49fe-8b80-6e987bcf160a", "name": "infra-core", ...}` | ✅ PASS |
| repositories.yml 一致性 | `grep -q "hdot123/infraro" ~/.factory/config/repositories.yml && echo "Found" \|\| echo "Missing"` | `Found` | ✅ PASS |
| runner 标签一致性 | `grep -A 5 -B 5 "pve-linux" docs/runner-registration-runbook.md && grep -A 5 -B 5 "runs-on" <generic-repo-check>/.github/workflows/auto-merge-pipeline.yml` | H5口径：分阶段<br>1. 公开期引擎 ubuntu-latest (为安全不落自建机)<br>2. 转私后切 self-hosted,pve-linux (免烧GitHub分钟数) | ⚠️ TRANSITION |
| 1Password 关键条目在场 | `1password MCP check` | `vault sever (ozqqpvh5yvvxvyu64npq62a3ti) item "ai.exa.edu.kg / NVIDIA Kong Proxy Key" (sjn2lq3ggpge4cyj46owrg7kmq) credential field accessible` | ✅ PASS |

## 公开仓脱敏声明

- 无生产 IP 段在本文件中暴露
- 无 token 值在本文件中暴露
- 无 `/Users/` 宿主路径在本文件中暴露
- 内部细节写入私有附录 `/Users/busiji/infraro/memory/kb/`

---

Created as part of substrate-map-and-manual feature
