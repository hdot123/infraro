"""droid-review-watchdog 触发器健康与运行时护栏契约测试（INFRA-1332）。

回归保护：watchdog 曾经整文件缺失（声明仓只保留模板、自用面裸奔），失败
review 无自愈、CI 红时 review 空烧 token。本套件锁定两件事：

1. 触发器健康基线：workflow_run 双监听（Droid Auto Review / CI completed）
   + schedule */30 必须在位——任一触发源被静默移除即红。
2. 七项运行时护栏（G1-G7，与 workflow 文件头编号注释一一对应）：
   G1 run_attempt 限界防 rerun 风暴
   G2 恢复窗口（配额未恢复不重试）
   G3 扫描窗口（旧失败不无限追溯）
   G4 事件精确门控（三 job 各自只由预期事件触发）
   G5 fail-closed（零 check 结论改写、零合并旁路 token）
   G6 超时上界（job 不挂死占 concurrency 组）
   G7 429 特征检测（transcript 签名为准，无签名不重试）
"""

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
WATCHDOG_PATH = REPO_ROOT / ".github" / "workflows" / "droid-review-watchdog.yml"

# 声明仓自用引擎锚（与 droid-review.yml 同仓 pin 面；模板面由发版公告链路齐步走）
ENGINE_HANDLERS_REF = (
    "hdot123/infraro-core-mirror/.github/workflows/"
    "droid-review-watchdog-handlers.yml@v0.24.0"
)


def _load() -> dict:
    return yaml.safe_load(WATCHDOG_PATH.read_text(encoding="utf-8"))


def _triggers(data: dict) -> dict:
    # YAML 1.1: bare `on:` parses as boolean True
    return data.get(True) or data.get("on") or {}


def _quota_sweep_run(data: dict) -> str:
    steps = data["jobs"]["quota-sweep"]["steps"]
    return steps[0]["run"]


def _all_run_blocks(data: dict) -> list[str]:
    blocks: list[str] = []
    for job in data["jobs"].values():
        for step in job.get("steps") or []:
            if step.get("run"):
                blocks.append(step["run"])
    return blocks


class TestTriggerHealthBaseline:
    """触发器健康基线（INFRA-1332 恢复动机：触发源曾在自用面整体缺失）。"""

    def test_workflow_file_present_on_live_face(self):
        """watchdog 必须在声明仓自用 workflows 目录在场（模板在位不算数）。"""
        assert WATCHDOG_PATH.is_file(), "live droid-review-watchdog.yml missing"

    def test_workflow_name_byte_exact(self):
        """VAL-GATE-107: workflow 名字节级为 'Droid Review Watchdog'。"""
        assert _load()["name"] == "Droid Review Watchdog"

    def test_workflow_run_listener_names_exact(self):
        """监听名集合精确 = {Droid Auto Review, CI}，types=[completed]（字节级）。"""
        wr = _triggers(_load())["workflow_run"]
        assert sorted(wr["workflows"]) == ["CI", "Droid Auto Review"]
        assert wr["types"] == ["completed"]

    def test_schedule_trigger_present(self):
        """schedule '*/30 * * * *' 在位（quota-sweep 唯一触发源）。"""
        assert _triggers(_load())["schedule"] == [{"cron": "*/30 * * * *"}]

    def test_concurrency_group_preserved(self):
        """concurrency 组锚定 workflow_run.id 且不取消进行中实例。"""
        conc = _load()["concurrency"]
        assert conc["group"] == "droid-review-watchdog-${{ github.event.workflow_run.id }}"
        assert conc["cancel-in-progress"] is False

    def test_listener_names_match_sibling_workflows(self):
        """监听名必须与本仓兄弟 workflow 实名一致（drift 即监听失效）。"""
        names = set()
        for wf in ("droid-review.yml", "ci.yml"):
            doc = yaml.safe_load(
                (REPO_ROOT / ".github" / "workflows" / wf).read_text(encoding="utf-8")
            )
            names.add(doc["name"])
        assert names == {"Droid Auto Review", "CI"}


class TestGuardrailG1AttemptLimit:
    """G1: run_attempt 限界防 rerun 风暴。"""

    def test_self_heal_forwards_max_attempt_with_default(self):
        """self-heal-rerun 以 max_attempt 转发 vars.WATCHDOG_MAX_ATTEMPT，缺省回退 3。"""
        job = _load()["jobs"]["self-heal-rerun"]
        assert job["with"]["max_attempt"] == "${{ vars.WATCHDOG_MAX_ATTEMPT || '3' }}"

    def test_quota_sweep_enforces_attempt_limit(self):
        """quota-sweep 循环内 attempt >= WATCHDOG_MAX_ATTEMPT 时跳过。"""
        run = _quota_sweep_run(_load())
        assert '"$ATTEMPT" -ge "$WATCHDOG_MAX_ATTEMPT"' in run
        assert "WATCHDOG_MAX_ATTEMPT=3" in run  # 变量缺失回退默认值

    def test_quota_sweep_forwards_attempt_var(self):
        """WATCHDOG_MAX_ATTEMPT 从 repo vars 注入 env（不硬编码取值）。"""
        env = _load()["jobs"]["quota-sweep"]["steps"][0]["env"]
        assert env["WATCHDOG_MAX_ATTEMPT"] == "${{ vars.WATCHDOG_MAX_ATTEMPT }}"


class TestGuardrailG2RecoveryWindow:
    """G2: 恢复窗口——配额未恢复时不重试。"""

    def test_recovery_window_uses_vars_with_default(self):
        """恢复窗口经 QUOTA_RECOVERY_WINDOW_SECONDS 配置，缺省 1800s。"""
        run = _quota_sweep_run(_load())
        assert "QUOTA_RECOVERY_WINDOW_SECONDS" in run
        assert "QUOTA_RECOVERY_WINDOW_SECONDS=1800" in run
        assert '-lt "$QUOTA_RECOVERY_WINDOW_SECONDS"' in run

    def test_quota_sweep_gated_on_schedule_event(self):
        """quota-sweep 仅 schedule 事件运行（立即 rerun 无意义，必须走恢复窗口）。"""
        assert _load()["jobs"]["quota-sweep"]["if"] == "github.event_name == 'schedule'"


class TestGuardrailG3ScanWindow:
    """G3: 扫描窗口——只扫最近 N 小时的失败 run。"""

    def test_scan_window_uses_vars_with_default(self):
        """扫描窗口经 QUOTA_SCAN_WINDOW_HOURS 配置，缺省 6 小时。"""
        run = _quota_sweep_run(_load())
        assert "QUOTA_SCAN_WINDOW_HOURS" in run
        assert "QUOTA_SCAN_WINDOW_HOURS=6" in run
        assert "hours ago" in run  # 以窗口构造 CUTOFF 而非全量扫描

    def test_failed_run_filter_by_exact_name_and_cutoff(self):
        """失败 run 过滤：name == "Droid Auto Review" 精确名 + CUTOFF 时间界。"""
        run = _quota_sweep_run(_load())
        assert '.name == \\"Droid Auto Review\\"' in run
        assert "$CUTOFF" in run


class TestGuardrailG4EventGating:
    """G4: 事件精确门控（github 事件上下文只在 caller 求值，必须留在本文件）。"""

    def test_self_heal_scoped_to_review_failure(self):
        """self-heal-rerun 仅 'Droid Auto Review' + conclusion failure 触发。"""
        cond = str(_load()["jobs"]["self-heal-rerun"]["if"])
        assert "github.event.workflow_run.name == 'Droid Auto Review'" in cond
        assert "github.event.workflow_run.conclusion == 'failure'" in cond

    def test_cancel_scoped_to_ci_failure(self):
        """cancel-on-ci-fail 仅 'CI' + conclusion failure 触发。"""
        cond = str(_load()["jobs"]["cancel-on-ci-fail"]["if"])
        assert "github.event.workflow_run.name == 'CI'" in cond
        assert "github.event.workflow_run.conclusion == 'failure'" in cond

    def test_job_topology_three_jobs(self):
        """恰好三个 job：两个引擎委托 handler + 本地 quota-sweep。"""
        assert set(_load()["jobs"]) == {"self-heal-rerun", "cancel-on-ci-fail", "quota-sweep"}

    def test_handler_jobs_delegate_to_engine(self):
        """两个 handler 纯 uses 委托引擎 handlers，执行体不在 caller 内联。"""
        data = _load()
        for job_name in ("self-heal-rerun", "cancel-on-ci-fail"):
            job = data["jobs"][job_name]
            assert job["uses"] == ENGINE_HANDLERS_REF, f"{job_name} 引擎锚漂移"
            assert job.get("steps") is None, f"{job_name} 不得保留内联执行体"
            assert job["permissions"] == {"actions": "write"}
            assert job["with"]["mode"] == job_name
            assert job["with"]["run_id"] == "${{ github.event.workflow_run.id }}"
            assert job["with"]["run_attempt"] == "${{ github.event.workflow_run.run_attempt }}"
            assert job["with"]["head_sha"] == "${{ github.event.workflow_run.head_sha }}"

    def test_top_level_permissions_minimal(self):
        """顶层权限恰为 actions: write（watchdog 只调 rerun/cancel API）。"""
        assert _load()["permissions"] == {"actions": "write"}


class TestGuardrailG5FailClosed:
    """G5: fail-closed——只请求 rerun/cancel，不改写 check 结论、零合并旁路。"""

    def test_no_check_conclusion_rewrite(self):
        """不出现任何 check 结论改写 API 面。"""
        for block in _all_run_blocks(_load()):
            for forbidden in ("check-runs", "annotations", "--admin", "--force"):
                assert forbidden not in block, f"forbidden token: {forbidden}"

    def test_no_merge_bypass_token(self):
        """caller 全 run block 零 merge 旁路 token（含 quota-sweep 本地 job）。"""
        for block in _all_run_blocks(_load()):
            assert "merge" not in block

    def test_rerun_uses_failed_jobs_api(self):
        """rerun 走 rerun-failed-jobs API（目标 run 终态后才可用）。"""
        assert "rerun-failed-jobs" in _quota_sweep_run(_load())


class TestGuardrailG6TimeoutBound:
    """G6: 超时上界——job 不挂死占 concurrency 组。"""

    def test_quota_sweep_timeout_bounded(self):
        """quota-sweep timeout-minutes <= 15。"""
        assert _load()["jobs"]["quota-sweep"]["timeout-minutes"] <= 15

    def test_handler_delegation_implies_engine_timeout(self):
        """handler job 为纯 uses 委托（超时由引擎 handlers 自带 10/5min 上界）。"""
        for job_name in ("self-heal-rerun", "cancel-on-ci-fail"):
            job = _load()["jobs"][job_name]
            assert job.get("uses"), f"{job_name} 必须委托引擎（超时随引擎面）"


class TestGuardrailG7QuotaSignature:
    """G7: 429 特征检测——transcript 签名为准，无签名不重试。"""

    def test_artifact_signature_grep(self):
        """检测必须 grep transcript 的 quota exceeded 签名（job log 无此特征）。"""
        run = _quota_sweep_run(_load())
        assert "quota exceeded" in run
        assert ".factory/sessions/" in run

    def test_artifact_prefix_filter_in_caller(self):
        """VAL-GATE-107: droid-review-debug- 前缀过滤保留在 caller 可断言。"""
        run = _quota_sweep_run(_load())
        assert 'startswith("droid-review-debug-")' in run

    def test_no_signature_no_rerun(self):
        """无签名分支明确 no auto-rerun（fail-closed 语义可断言）。"""
        assert "no quota signature in transcript. Not quota-related; no auto-rerun." in _quota_sweep_run(_load())


class TestGuardrailDocAnchors:
    """文件头 G1-G7 编号注释与实现同在（护栏可读性锚点）。"""

    def test_numbered_guardrail_comments_present(self):
        """文件头必须含 G1-G7 全部七条编号护栏注释。"""
        text = WATCHDOG_PATH.read_text(encoding="utf-8")
        for marker in ("G1", "G2", "G3", "G4", "G5", "G6", "G7"):
            assert f"{marker} " in text or f"{marker}：" in text, f"护栏编号注释缺失: {marker}"
