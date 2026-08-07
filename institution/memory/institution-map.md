---
name: institution-map
description: 跨專案制度的結構指標——架構描述唯一正本在 claude-institution repo 的 README.md
metadata: 
  node_type: memory
  type: project
  originSessionId: 4dd139ff-7dd8-4f89-9410-a331472fcb05
---

Curtis 的跨專案制度：正本在 `~/.claude/`（CLAUDE.md 索引；`rules/` 下 `hard-rules.md`／
`code-standards.md` 無 `paths:` frontmatter，Claude Code 自動常載，不需 `@import`；
`rules-lib/` 按需；skills/ 3 個；hooks/ 5 個層 0 腳本；agents/ 3 個對抗審查 subagent——
該目錄是第三方 wshobson/agents 的 git clone，3 檔已加 `.git/info/exclude`）。
2026-08-06 用 `eval/` 對 Opus 5 實測一輪後精簡：刪 `diagnosis.md`、`hard-rules.md` #14；
XY problem 核心判準搬進 CLAUDE.md 起手式常載（原按需檔 `intake.md` 觸發機制實測不可靠）。
災難還原與完整架構說明的**唯一正本**＝claude-institution repo（README.md + restore.sh），
不在此重述以免漂移。新規則放哪層看 CLAUDE.md 分層表；改制度檔前讀 rules-lib/maintenance.md。
