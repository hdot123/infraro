# Substrate Gate Registry — declaration repository (hdot123/infraro)

存量登记表：五道门首跑如实暴露的存量红项，逐条登记 owner + 归属 feature。
「门先红着上线」裁定（substrate-gate-suite，2026-09-13）：门照常运行并如实
输出红/绿；存量红项不阻断合并（advisory），由下列归属 feature 清理后转绿；
门全绿后由 misc feature 统一转正 required checks（解冻判据③）。

豁免 = 登记 + owner。未经本表登记的新红项一律 FAIL。

## Gate 0: coverage completeness（覆盖完备性豁免区）

| Entry | Reason | Owner | Owning feature | Detail |
|---|---|---|---|---|
| `LICENSE` | static legal text | hdot123 | engine-substrate-boundary | 静态法律文本，无质量门域；随 boundary 画线裁定归属 |
| `tools` | shellcheck/ruff advisory linters added (ci.yml advisory steps) | hdot123 | substrate-inventory-bookkeeping | 声明仓 CI 已补 shellcheck/ruff advisory jobs（continue-on-error 形态） |
| `scripts` | shellcheck/ruff advisory linters added (ci.yml advisory steps) | hdot123 | substrate-inventory-bookkeeping | 声明仓 CI 已补 shellcheck/ruff advisory jobs（continue-on-error 形态） |

## Gate 1: registered interface stock（模板调用面存量）

| Template | Break | Owner | Owning feature | Detail |
|---|---|---|---|---|
| `watchdog.yml` | per-key | hdot123 | declaration-template-interface-fix | 传未声明键 engine_ref + 未声明 secrets dispatch_token/dispatch-token + 缺必填 mode/run_id/run_attempt（run 级 startup_failure） |

## Gate 2: cross-repo inspection stock

门2 cron 巡检为引擎仓 workflow（gate2-cross-repo-inspection.yml）所有；
声明仓不重复承载。声明仓侧关联存量（首跑引擎侧输出）见引擎仓
`substrate/gate0-exemptions.md` Gate 2 节（memory 冻结仓残留分支/在途 PR、
repositories.yml 补登、ERROR_REPO_MAP 双侧一致性）。

## Gate 3: exposure scan stock（敏感面存量 + 自引用排除）

| Entry | Reason | Owner | Owning feature | Detail |
|---|---|---|---|---|
| `docs/substrate-map.md:98 local-path` | stock | hdot123 | substrate-inventory-bookkeeping | 手册「公开仓脱敏声明」自述无 /Users/ 路径但下一行暴露私有附录宿主路径；改相对引用 `memory/kb/` |
| `substrate/gates/（扫描器自引用）` | self-reference | hdot123 | substrate-gate-suite（本 suite 自有） | 门套件自身正则字面量含 /Users/、/home/ 扫描模式；对 substrate/gates/ 自引用行显式排除，此处登记备案 |

Accepts（非暴露，不登记为存量）：`/Users/runner`、`/home/runner`（GitHub
托管 runner 家目录）；`@users.noreply.github.com`/example 邮箱；RFC 5737
文档 IP 段；prose 中「1Password」产品名词（暴露形态是 op:// 条目引用 URI，
已按 op:// 形态扫描）.

## Gate 4

断言编码与 bootstrap 一键拉起为引擎仓所有（`substrate/gates/
gate4_timing_bootstrap.py` + `scripts/bootstrap-substrate.sh`）；声明仓侧
仅经引擎门4 的 declaration-substrate-manual 检查项间接覆盖（substrate-map
在场性），无独立存量.
