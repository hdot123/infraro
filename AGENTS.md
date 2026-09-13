<!-- MEMORY_HOOK_BEGIN -->
## Memory Hook

This project uses the memory-core protected wrapper for hooks.
The wrapper is installed at `~/.factory/bin/memory-hook` and handles:

- Project lifecycle tracking
- HOME directory anti-pollution guards
- Source repository detection (skips memory-core itself)
- Git root normalization

Project memory rules are stored under `memory/` and loaded regardless of host.
Do NOT use bare `memory-hook-gateway` commands directly.

For manual testing:

```bash
~/.factory/bin/memory-hook --host factory --event session-start
```

## 路由规则

路由规则仅由以下文件定义，AGENTS.md 只做方向性引用，不嵌入任何路由逻辑。

**读取链**：Agent 启动 → AGENTS.md (行为约束) → 三层架构路由 → Layer 3 项目层优先 → Layer 2 全局 fallback

| 层 | 职责 | 路径 |
|----|------|------|
| 全局知识库 (Layer 2) | 跨项目通用知识、全局 fallback | `~/.memory/global-kb/` |
| 项目知识库 (Layer 3) | 项目专属知识 | `<project>/memory/kb/` |

具体路由规则（如 scope resolution、fallback）请查阅上述路径下的 INDEX.md。

## 执行前置规则

**任何涉及知识库的读取或写入操作前，必须先读取本文件确认术语到路径的映射。不可凭记忆或上下文推断路径。**

| 操作场景 | 前置要求 |
|----------|----------|
| 写入 `memory/kb/`、`docs/`、`~/.memory/global-kb/` | 先查路由表确认目标层和正确路径 |
| 读取项目知识库 | 先确认 Layer 3 → Layer 2 fallback 顺序 |
| 用户说"记下来"/"写文档"/"记录决策" | 先读项目 AGENTS.md 确认分类规则，再执行写入 |

<!-- MEMORY_HOOK_END -->
