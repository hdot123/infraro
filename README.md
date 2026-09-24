# infraro

声明层：规则包规范、消费仓接入指南、Workflow 模板、API 参考的公开文档面。声明本体随各消费仓走，本仓为规范与模板真源。

## 双栈模板（当前锚 @v0.18.9）

消费仓接入按语言栈各取一套模板，两栈内容对齐、锚点一致（全部 `@v0.18.9`）：

- **Python 栈**：[templates/python/](templates/python/)
- **TypeScript 栈**：[templates/typescript/](templates/typescript/)

每栈 7 件套 workflow 模板（5 thin-caller + 2 copy-form）+ 栈内配套文件：

| 类别 | 文件 | 形态 |
|------|------|------|
| thin-caller | `evolution-scan.yml` / `evolution-heartbeat.yml` / `auto-merge.yml` / `droid-review.yml` / `droid-review-watchdog.yml` | `uses@v0.18.9` tag 锚 |
| copy-form | `governance.yml` / `branch-cleanup.yml` | 溯源头 + composite action SHA 钉 |
| 栈内配套 | `.github/workflows/ci.yml`、`.github/actionlint.yaml`、`.evolution/`（config + suppress） | 随栈整取 |

锚点纪律：thin-caller 全锚（engine=workflow=同 tag），全仓禁止 `@main`。引擎升级由发版公告链路自动派发 pin-bump PR（release-gateway），齐步走到新 tag。

## 引擎安装（匿名免认证）

```bash
pip install git+https://github.com/hdot123/infraro-core.git@v0.18.9
```

引擎为公开仓 `hdot123/infraro-core`，git+https 匿名拉取，无需任何 token。

## Secrets（snake 单形态，三件）

消费仓需配置的 org/repo secrets（只列名，值零入仓）：

- `NVIDIA_KONG_PROXY_KEY` — droid-review 自定义模型 apiKey（lumivane CF AiGateway 双头之一）
- `LUMIVANE_CFAT` — `cf-aig-authorization: Bearer <...>` 头（双头之二）
- `FACTORY_API_KEY` — droid 会话触发

历史形态（`LUMIVANE_BASE_URL`、旧端点 `ai.exa.edu.kg` 三 secret 形态）已废弃，模板中不再引用。

## Runner 拓扑（born-complete 标配）

- **hosted 常规测试槽**：CI/QA 常规 job 走 GitHub hosted runner
- **ce-01 自建 runner 重负载槽**：droid-review / governance / scan / heartbeat 走自建 runner，labels `self-hosted,pve-linux`

## 分支保护

消费仓 ruleset：required checks = `[ci-ok]`（工作流名 `CI`，job key `ci-ok`），squash-only 合并。

## Documentation

- [Architecture（四组件架构，所有者裁定 v2 对齐）](docs/architecture.md)
- [Getting Started](docs/getting-started.md)
- [Consumer Onboarding Guide](docs/consumer-onboarding.md)
- [Naming Contracts](docs/naming-contracts.md)
- [Base Layer Templates](docs/base-layer-templates.md)

## Templates

- [Workflow Templates](templates/) — 双栈目录 `templates/python/` 与 `templates/typescript/`（@v0.18.9）；根下单栈历史存档已删除（陈旧 @v0.18.5 形态，双栈为其 supersede）
