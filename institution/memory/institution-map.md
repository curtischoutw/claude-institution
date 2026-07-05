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

**Why:** Curtis 之後長期由較弱模型服務；制度必須是可機械執行的 if-then + 範本 + 分層強制。
**How to apply:** 新規則照 CLAUDE.md 分層表選載體；改制度檔前讀 maintenance.md 的權限分級；
@import 已於 2026-07-05 以 `claude -p` 全新 session 實測生效；僅剩「Opus 4.8 導流是否
吃額度」未確認，見 letter-to-future.md。另有 rules/uplift.md（判斷力增強協定）。
