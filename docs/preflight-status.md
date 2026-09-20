# Preflight Status Copy Spec（三态文案规范）

声明层规范：消费仓接入与排障时的 preflight 三态文案。所有模板与文档统一引用本规范，
不得自造口径。真源 = `hdot123/scheduler` 仓 `authorized.yaml`（引擎消费白名单唯一授权入口）。

## 三态定义与文案

| 态 | 触发条件 | 文案基调 | 指向 |
|----|----------|----------|------|
| 待申请（中性指引） | 仓不在白名单，尚无任何通道腿 | 中性：指引走授权流程，不渲染为故障 | `hdot123/scheduler` 的 `authorized.yaml` PR |
| 权限故障（红指 owner） | PAT 不可达 / token 缺权 / secret 未铺 | 红：明确是 owner 侧凭证面问题，消费仓无法自愈 | owner（scheduler 仓维护者） |
| 已授权缺配（红指 sync） | 白名单已列但腿未铺齐（variable / secret / runner 有缺） | 红：授权已批但同步未落地，指 whitelist-sync | scheduler 仓 whitelist-sync（plan → apply） |

## 标准文案模板

**待申请**（管线入口守卫 fail 时的用户面指引）：

> 未授权消费引擎，走授权流程：本仓未设置 repo variable `ENGINE_CONSUMERS`
> （授权四步：variable → PAT → runner → 6 阶段验收）。
> 申请入口：向 [hdot123/scheduler](https://github.com/hdot123/scheduler/blob/main/authorized.yaml)
> 的 `authorized.yaml` 提 PR 加一行本仓名，合并后由 whitelist-sync 铺设通道。

**权限故障**（红，指 owner）：

> 🔴 授权状态不可读 / PAT 不可达：这是 scheduler 侧凭证面问题（PAT 收权、过期或缺
> Variables 读权限），消费仓无法自愈。请 owner 检查 `SCHEDULER_TOKEN` 对应 PAT
> （1Password `GitHub-PAT-A-Z`）的仓库范围与权限面。

**已授权缺配**（红，指 sync）：

> 🔴 白名单已列本仓但通道未铺齐（对照 pinned Issue「白名单对账 · 每日状态」的
> 🟡 待同步行）。请到 scheduler 仓跑 whitelist-sync：mode=plan 拿计划书与
> plan_hash → mode=apply 落地。

## 消费者侧自查入口

- 白名单真源：`https://github.com/hdot123/scheduler/blob/main/authorized.yaml`
- 加仓 PR 路径：`https://github.com/hdot123/scheduler/compare/main...main?expand=1`（编辑 `authorized.yaml`）
- 对账状态：scheduler 仓 pinned Issue「白名单对账 · 每日状态」（三态判定 + SHA 锚定）
- 两段式同步：scheduler 仓 Actions → whitelist-sync（workflow_dispatch：mode/plan_hash/force_removals）
