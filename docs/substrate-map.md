# Substrate 总账 + 标准手册

**F3.5 首交付物**：基础层资产总账与处置手册，确保零污染进入新世界。

## 1. 记忆/知识系统 (ACTIVE)

| 组件 | 所在仓/位置 | 世界归属 | 状态 | 处置结论 | Owner |
|------|-------------|----------|------|----------|-------|
| memory 仓 | hdot123-org/memory | 旧世界 | RETIRED | [RETIRE] → 指向 memory-core | hdot123 |
| memory-core wrapper | `~/.factory/bin/memory-hook` | 新世界 | ACTIVE | 保留 | hdot123 |
| `~/.memory-core` | host filesystem | 新世界 | ACTIVE | 保留 | hdot123 |
| global-kb 仓 | hdot123-org/global-kb | 旧世界 | RETIRED | [RETIRE] → 指向 infraro knowledge layer | hdot123 |
| `~/.memory/global-kb` | host filesystem | 新世界 | ACTIVE | 保留 | hdot123 |
| 各项目 memory/ | `<project>/memory/` | 混合 | ACTIVE | 保留 | 项目 owner |

### 拉起步骤与验收条目（记忆系统）

#### 记忆系统拉起步骤

1. 确保 `~/.factory/bin/memory-hook` 存在且可执行
2. 确保 `~/.memory-core` 目录结构完整
3. 验证项目记忆系统可正常读写：`~/.factory/bin/memory-hook --host infraro --event session-start`

#### 记忆系统验收条目

- [ ] `~/.factory/bin/memory-hook` 存在且可执行
- [ ] `~/.memory-core` 目录存在且包含必要的 hook 文件
- [ ] `~/.memory/global-kb` 目录存在
- [ ] 项目记忆系统读写操作正常

## 2. Factory 运行时 (ACTIVE)

| 组件 | 所在仓/位置 | 世界归属 | 状态 | 处置结论 | Owner |
|------|-------------|----------|------|----------|-------|
| `~/.factory` | host filesystem | 新世界 | ACTIVE | 保留 | hdot123 |
| hooks | `~/.factory/hooks` | 新世界 | ACTIVE | 保留 | hdot123 |
| missions | `~/.factory/missions` | 新世界 | ACTIVE | 保留 | hdot123 |
| config/repositories.yml | `~/.factory/config/repositories.yml` | 新世界 | ACTIVE | 收编 | hdot123 |
| webhook 脚本 | `~/.factory/webhook/scripts` | 新世界 | ACTIVE | 保留 | hdot123 |

### 拉起步骤与验收条目（Factory 运行时）

#### Factory 运行时拉起步骤

1. 确保 `~/.factory` 目录结构完整
2. 确保 hooks 在 `~/.factory/hooks` 中可用
3. 验证 mission 系统可正常运行：`droid exec --skill mission-worker-base`

#### Factory 运行时验收条目

- [ ] `~/.factory` 目录存在
- [ ] `~/.factory/hooks` 目录存在且包含 hook 脚本
- [ ] `~/.factory/missions` 目录存在
- [ ] webhook 脚本可执行
- [ ] Mission 系统可正常启动和运行

## 3. 通知链（webhook 全链路 - ACTIVE）

| 组件 | 所在仓/位置 | 世界归属 | 状态 | 处置结论 | Owner |
|------|-------------|----------|------|----------|-------|
| hdot123/webhook (CF Worker) | ci-webhook.exa.edu.kg | 旧世界 | ACTIVE | 收编 | hdot123 |
| 本地 webhook 脚本 | `~/.factory/webhook/scripts/` | 新世界 | ACTIVE | 保留 | hdot123 |
| pending 文件 | `~/.factory/webhook/locks/` | 新世界 | ACTIVE | 保留 | hdot123 |

### 拉起步骤与验收条目（通知链）

#### 通知链拉起步骤

1. 确保 CF Worker (ci-webhook.exa.edu.kg) 可访问
2. 验证本地 webhook 脚本存在且可执行
3. 验证 locks 目录存在且可写

#### 通知链验收条目

- [ ] CF Worker 服务可访问（curl -s -o /dev/null -w "%{http_code}" <https://ci-webhook.exa.edu.kg/health>）
- [ ] `~/.factory/webhook/scripts` 目录存在且脚本可执行
- [ ] `~/.factory/webhook/locks/` 目录存在且可写
- [ ] webhook 脚本功能正常（pending-ci registration/delivery）

## 4. Runner 机队 (ACTIVE)

| 组件 | 所在仓/位置 | 世界归属 | 状态 | 处置结论 | Owner |
|------|-------------|----------|------|----------|-------|
| ce-01 | GitHub Actions | 新世界 | ACTIVE | 分阶段处置：公开期引擎 ubuntu-latest；引擎转私有仓后切 self-hosted,pve-linux（已记录在 runbook 迁移清单） | hdot123 |
| pve-runner-01..06 | 自建服务器 | 新世界 | ACTIVE | 保留 | hdot123 |

### 拉起步骤与验收条目（Runner 机队）

#### Runner 机队拉起步骤

1. 验证 ce-01 runner 在 GitHub Actions 中注册
2. 验证自建服务器 runners pve-runner-01..06 运行正常

#### Runner 机队验收条目

- [ ] 引擎公开期 CI 用 hosted runner 口径（自声明仓克隆根执行）：`grep -n "runs-on: ubuntu-latest" ../infraro-core/.github/workflows/ci.yml`（实测 :46/:97/:218 命中）
- [ ] 消费仓 self-hosted runners（F4 注册后验收，当前不执行）：`gh api repos/hdot123/<consumer>/actions/runners --jq .total_count`（≥1 为通过；F4 前无消费仓。勿对引擎仓执行——其 runners API 为 hosted-only，total_count=0 属实测口径）
- [ ] Runners have correct labels (self-hosted, pve-linux)
- [ ] 分阶段策略正确实施（公开期使用 ubuntu-latest，私有后切换）

## 5. 遗留模板仓 (ARCHIVED)

| 组件 | 所在仓/位置 | 世界归属 | 状态 | 处置结论 | Owner |
|------|-------------|----------|------|----------|-------|
| ci-templates | hdot123/ci-templates | 旧世界 | ARCHIVED | [RETIRE] → 已归档 | hdot123 |
| gitlab-ci-standards | hdot123/gitlab-ci-standards | 旧世界 | ARCHIVED | [RETIRE] → 已归档 | hdot123 |
| workflows-starter-template | hdot123/workflows-starter-template | 旧世界 | ARCHIVED | [RETIRE] → 已归档 | hdot123 |

## 6. 遗留基础设施 (MIXED)

| 组件 | 所在仓/位置 | 世界归属 | 状态 | 处置结论 | Owner |
|------|-------------|----------|------|----------|-------|
| gh-proxy | `hdot123/infraro-core/cf/gh-proxy` | 旧世界 | ACTIVE | 迁出 | hdot123 |
| gateway-admin | hdot123/gateway-admin | 旧世界 | INACTIVE | [RETIRE] | hdot123 |

### 拉起步骤与验收条目（遗留基础设施）

#### 遗留基础设施拉起步骤

1. 仓内真源：引擎仓 `cf/gh-proxy/DEPLOYMENT.md` 与 `cf/gh-proxy/wrangler.toml`（部署细节以二者为准，本节为其摘要）
2. 在引擎仓克隆根进入目录：`cd cf/gh-proxy`
3. 部署 Worker（需先设置 Cloudflare API Token）：`npx wrangler deploy`
4. 设置环境变量和 secrets：

   ```bash
   printf 'value-from-1password' | npx wrangler secret put PROXY_KEY
   printf 'ghp_xxxx' | npx wrangler secret put GH_PRIVATE_PAT
   ```

5. 验证 gateway-admin 已废弃

#### 遗留基础设施验收条目

- [ ] Cloudflare Worker gh-proxy successfully deployed
- [ ] PROXY_KEY and GH_PRIVATE_PAT secrets properly set
- [ ] Worker accessible at configured custom domain
- [ ] gateway-admin no longer active
- [ ] Test requests succeed: `curl -H "x-proxy-key: $PROXY_KEY" "https://gh.qqbaidu.de5.net/https://github.com/actions/checkout"`

## 7. Linear 工作面

| 组件 | 所在仓/位置 | 世界归属 | 状态 | 处置结论 | Owner |
|------|-------------|----------|------|----------|-------|
| Linear workspace | hdot123 Linear workspace | 混合 | ACTIVE | 新建 v3 项目 "infraro v3" (ID: 3c2927a2-6b8d-4dda-af6b-3cf27310952a)，旧项目 4b08a1b7 冻结零触碰 | hdot123 |

### Linear 团队与项目分类

| 团队/项目 | 世代分类 | 活跃状态 | 处置结论 |
|----------|----------|----------|----------|
| INFRA team | 旧世界 | 活跃 | 保持运营 |
| DEFAULT team | 旧世界 | 部分取消 | 9个已取消项目，保持运营 |
| WORKBOT team | 旧世界 | 活跃 | 保持运营 |
| GW team | 旧世界 | 活跃 | 保持运营 |
| TES team | 测试演示 | 活跃 | 保持运营 |
| 优志愿(YZ) team | 业务 | 活跃 | 按业务状态管理 |
| 教学(JX) team | 业务 | 活跃 | 按业务状态管理 |
| 题库(TIKU) team | 业务 | 活跃 | 按业务状态管理 |
| infra-core 项目 | 旧世界 | 活跃（冻结） | 冻结零触碰 |
| infraro v3 项目 | 新世界 | 活跃 | 新项目持续运营 |
| youzy 项目 | 业务 | 活跃 | 按业务状态管理 |
| jiaoxue 项目 | 业务 | 活跃 | 按业务状态管理 |
| tiku 项目 | 业务 | 活跃 | 按业务状态管理 |

### Linear 引擎仓变量验证

| Variable | Value | Status |
|----------|-------|--------|
| LINEAR_PROJECT_INFRA_CORE_ID | 4b08a1b7-1382-49fe-8b80-6e987bcf160a | 已验证 |
| LINEAR_PROJECT_INFRARO_V3_ID | 3c2927a2-6b8d-4dda-af6b-3cf27310952a | 已验证 |

### 拉起步骤与验收条目（Linear）

#### Linear 拉起步骤

1. 验证 Linear 连接器可用性
2. 检查项目和团队状态
3. 验证变量配置正确

#### Linear 验收条目

- [ ] Linear 连接器可正常访问
- [ ] infraro v3 项目存在且 ID 为 3c2927a2-6b8d-4dda-af6b-3cf27310952a
- [ ] 旧项目 infra-core 冻结且 ID 为 4b08a1b7-1382-49fe-8b80-6e987bcf160a
- [ ] 引擎仓变量 LINEAR_PROJECT_* 配置正确

## 8. 基础检查（探针集）

以下为基础检查探针的实跑结果.

| 探针类型 | 命令 | 实际输出 | 期望输出 | 状态 |
|----------|------|----------|----------|------|
| webhook 链端到端 | `curl -s -o /dev/null -w "%{http_code}" <https://ci-webhook.exa.edu.kg/health>` | `000（2026-09-14 复测：连接超时 exit 28；2026-09-13 时点为 502）` | `200` | ⚠️ 持续不可达（恢复侧证据：gate2 cron 成功 run；已列待用户项） |
| Linear key 只读探针 | `linear__get_project --id 4b08a1b7-1382-49fe-8b80-6e987bcf160a` | `{"id": "4b08a1b7-1382-49fe-8b80-6e987bcf160a", "name": "infra-core", ...}` | `Valid project response with matching ID` | ✅ PASS |
| repositories.yml 一致性 | `grep -q "hdot123/infraro" ~/.factory/config/repositories.yml && echo "Found" \|\| echo "Missing"` | `Found` | `Found` | ✅ PASS |
| runner 标签一致性 | `grep -A 5 -B 5 "pve-linux" docs/runner-registration-runbook.md && grep -A 5 -B 5 "runs-on" ../infraro-core/.github/workflows/auto-merge-pipeline.yml`（自声明仓克隆根执行，引擎克隆为同级目录） | H5口径：分阶段<br>1. 公开期引擎 ubuntu-latest (为安全不落自建机)<br>2. 转私后切 self-hosted,pve-linux (免烧GitHub分钟数) | 分阶段策略验证通过 | ⚠️ TRANSITION |
| 1Password 关键条目在场 | `1password-connect___search_items vault=sever query="ai.lumivane.dpdns.org / NVIDIA Kong Proxy"`（MCP 规范工具名形态，validator 经 MCP 执行；名称级在场性，不取值） | `sever vault 条目 "ai.lumivane.dpdns.org / NVIDIA Kong Proxy Key" 命中` | `Valid access to required items` | ✅ PASS |
| Worker secrets 存在性 | `1password-connect___search_items vault=sever query="CF Worker / POSTHOG_TOKEN"`（MCP 规范工具名形态；逐名结果见 §9 表） | POSTHOG_TOKEN 条目 found, others missing | All 6 items available | ❌ BLOCKED (无 CF API token；实面核验需用户提供 scoped API token 或裁定 Dash 登录路线——转用户裁定，worker 不自行登录 Dash) |

## 9. Worker Secrets 验证

以下为 CF Worker secrets 约定条目在场性验证结果（1Password 条目检索）：

| Secret 名 | 在场性 | 1Password 条目名 | 备注 | 验证时间 |
|----------|--------|------------------|------|----------|
| CI_TOKEN | 缺失 | 未找到匹配条目 | 未在 vault sever 中找到约定条目 | 2026-09-14 |
| GITHUB_WEBHOOK_SECRET | 缺失 | 未找到匹配条目 | 未在 vault sever 中找到约定条目 | 2026-09-14 |
| LINEAR_WEBHOOK_TOKEN | 缺失 | 未找到匹配条目 | 未在 vault sever 中找到约定条目 (Linear API tokens exist but not webhook-specific) | 2026-09-14 |
| POSTHOG_CAPTURE_KEY | 缺失 | 未找到匹配条目 | 未在 vault sever 中找到约定条目 | 2026-09-14 |
| POSTHOG_TOKEN | 在场 | CF Worker / POSTHOG_TOKEN / webhook (ci-webhook.exa.edu.kg) | 约定条目存在 | 2026-09-14 |
| WIKI_TOKEN | 缺失 | 未找到匹配条目 | 未在 vault sever 中找到约定条目 | 2026-09-14 |

### CF Worker 实面核验状态

❌ BLOCKED - 无 CF API token 条目在 vault sever 中。实面核验需用户提供 scoped API token 或裁定 Dash 登录路线——转用户裁定，worker 不自行登录 Dash。

### ERROR_REPO_MAP 详细验证

| 项 | 映射 | 处置状态 | 备注 |
|----|------|----------|------|
| infra_core | hdot123-org/infra-core | 冻结仓库 | 指向旧世界冻结仓库，已知且接受 |
| memory_core | hdot123-org/memory | 冻结仓库 | 指向旧世界冻结仓库，已知且接受 |
| memory | hdot123-org/memory | 冻结仓库 | 指向旧世界冻结仓库，已知且接受 |
| mencbo | hdot123-org/mencbo | 冻结仓库 | 指向旧世界冻结仓库，已知且接受 |
| infraro_core | hdot123/infraro-core | 新世界 | 指向新世界引擎仓库，正确配置 |

### Strict Mode 状态验证

- **Worker 侧**: worker.js 中无 "strict" 概念；wrangler.toml [vars] 包含路由标志 R1_ROUTE_ERROR="true", R1_ROUTE_LINEAR="true" (worker.js:695/:864 gate the two dispatch chains).
- **引擎仓侧**: 仓库变量 WEBHOOK_NOTIFY_STRICT=true (2026-09-12T20:27:07Z 设置)，在 .github/workflows/ci.yml:688 消费并实施

### Pending-CI 链路验证

- `~/.factory/webhook/scripts/write-pending-ci.sh` 存在且可执行
- `~/.factory/webhook/scripts/trigger-ci-droid.sh` 存在且可执行  
- `~/.factory/webhook/locks/` 目录存在且活跃
- 链路演示：write-pending-ci -> lock file -> trigger-ci-droid 读取并注入消息

### 约定条目统计

- 约定条目总数：6
- 在场条目数：1 (POSTHOG_TOKEN)
- 缺失条目数：5
- CF Worker 实面核验：BLOCKED

### 冻结常量脚注

- ERROR_REPO_DEFAULT: 默认错误仓库配置常量
- EXECUTOR_HOST_REPO: 执行器主机仓库标识常量

## 公开仓脱敏声明

- 无生产 IP 段在本文件中暴露
- 无 token 值在本文件中暴露
- 无 1Password 条目 ID 在本文件中暴露
- 无 vault ID 在本文件中暴露
- 无 `/Users/` 宿主路径在本文件中暴露
- 内部细节写入私有附录 `memory/kb/`

---

Created as part of substrate-map-and-manual feature
