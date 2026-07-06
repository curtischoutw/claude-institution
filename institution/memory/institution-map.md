---
name: institution-map
description: 2026-07-05 Fable 5 session 建立的完整制度架構 v3：索引式 CLAUDE.md + rules/ 九檔 + 三 skill
metadata: 
  node_type: memory
  type: project
  originSessionId: 4dd139ff-7dd8-4f89-9410-a331472fcb05
---

Curtis 用唯一一次 Fable 5 session 建立跨專案制度（claude-institution 專案，2026-07-05 由
fable_once 改名，只是建制現場，無程式碼）。

**架構 v3**：`~/.claude/CLAUDE.md`（40 行純索引路由）@import `rules/hard-rules.md` 與
`rules/code-standards.md`（常載合計約 135 行）；按需檔在 `~/.claude/rules/`：
diagnosis（三大耗損源）、dispatch（模型調度守則，型號 2026-07-05 查證）、judgment
（五個 rubric）、prompt-templates（五種交辦範本）、maintenance（維護權限分級）、
letter-to-future（交接信，含未確認事項）。skill：done-check / lesson / debug-protocol。

全部產出經 fresh-context sonnet 對抗審查，6 處矛盾已修。備份在 `~/.claude/backups/`。

**2026-07-05 補充（同日稍後）：層 0 不再是空的**。借鑑 GitHub `Miguok/fable-harness`
（同日出現的另一套 Claude Code 紀律協定，機制相近但協定文字不同）補了兩個 hook：
`~/.claude/hooks/verify_gate.py`（Stop hook，動了程式碼卻無測試指令就擋下，指向
hard-rules #5 / `/done-check`，fail-open）與 `prompt_nudge.sh`（UserPromptSubmit，
每回合一行提醒）。同時加了三個對抗審查 subagent：`~/.claude/agents/{skeptic,red-team,
simplifier}.md`，對應 uplift.md 方法 2/3，可直接派發。**`~/.claude/agents/` 本身是
第三方 `wshobson/agents` 的 git clone**，三個新檔已加進該 clone 的
`.git/info/exclude` 避免污染。全部同步進 claude-institution repo 的
`institution/hooks/`、`institution/agents/` 快照，`restore.sh` 已更新涵蓋。

**Why:** Curtis 之後長期由較弱模型服務；制度必須是可機械執行的 if-then + 範本 + 分層強制。
**How to apply:** 新規則照 CLAUDE.md 分層表選載體；改制度檔前讀 maintenance.md 的權限分級；
@import 已於 2026-07-05 以 `claude -p` 全新 session 實測生效；僅剩「Opus 4.8 導流是否
吃額度」未確認，見 letter-to-future.md。另有 rules/uplift.md（判斷力增強協定），現可
搭配 [[skeptic]]/[[red-team]]/[[simplifier]] 三個 subagent 實際派發執行。
