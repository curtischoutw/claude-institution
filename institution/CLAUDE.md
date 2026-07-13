# AI Assistant Workflow Configuration（索引）

<!-- v3.0 (2026-07-05)：本檔只當索引路由，≤150 行；直接 @import 的常載檔合計 ≤500 行。
     新增內容一律寫新檔再在此加一行路由，不塞長內容進本檔。
     歷史版本在 ~/.claude/backups/。維護規約見 ~/.claude/rules/maintenance.md。 -->

## Session 起手式

1. 讀專案的 `tasks/lessons.md`（不存在就跳過，不要建立）。
2. 動手前一句話複述：任務範圍 + 完成判準。只有「走錯方向的代價 > 提問成本」才提問，
   否則寫下假設繼續做；開場提問一次問完（≤5 題），之後自主作業不停等。

## 路由表（遇到情境 → 讀對應檔或用 skill，再動手）

| 情境 | 去處 |
|---|---|
| 要派 subagent（讀多檔、搜尋、掃 repo、查網頁、批次改檔、驗證） | 讀 `~/.claude/rules/dispatch.md` |
| 寫交辦 prompt（搜尋/實作/重構/研究/審查） | 抄 `~/.claude/rules/prompt-templates.md` |
| 拿不定主意：升級模型？算完成？該問人？該換路？品質夠嗎？ | 讀 `~/.claude/rules/judgment.md` |
| 高風險判斷：架構決策、多方案取捨、規格模糊、難根因 | 讀 `~/.claude/rules/uplift.md` 照強度分級執行 |
| 準備宣稱「完成」或 commit | 用 skill `/done-check` |
| 除錯卡住、同一問題修 2 次沒好 | 用 skill `/debug-protocol` |
| 被使用者糾正 | 用 skill `/lesson` |
| 想修改 ~/.claude/ 下任何制度檔 | 先讀 `~/.claude/rules/maintenance.md` |
| 想了解本 harness 的 token/失焦/出錯風險 | 讀 `~/.claude/rules/diagnosis.md` |

## 制度分層（任何新規則先決定放哪層，能上不下）

| 層 | 載體 | 放什麼 |
|---|---|---|
| 0 | hooks / permissions（settings.json，用 /update-config） | 機器可判定的規則，最可靠 |
| 1 | 本檔 + @import 常載檔 | 每次必守、1–2 行寫得完的硬規則 |
| 2 | `~/.claude/skills/` 與 `~/.claude/rules/` 按需檔 | 多步驟程序、checklist、範例 |
| 3 | 專案 `tasks/lessons.md` | 糾正的第一落點；第 2 次觸發升級到層 0–2 |
| 4 | memory/ 目錄 | 只放事實與偏好，不放規則 |

## 常載規則（@import）

@~/.claude/rules/hard-rules.md

@~/.claude/rules/code-standards.md
