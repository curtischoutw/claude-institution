# AI Assistant Workflow Configuration（索引）

<!-- 本檔只當索引路由：新增內容一律寫新檔再在此加一行路由，不塞長內容進本檔。
     常載預算：本檔＋rules/ 合計 ≤200 行（比照官方 CLAUDE.md 建議上限）。
     維護規約見 ~/.claude/rules-lib/maintenance.md。 -->

## Session 起手式

1. 動手前一句話複述：任務範圍 + 完成判準。只有「走錯方向的代價 > 提問成本」才提問，
   否則寫下假設繼續做。
2. XY problem 快速檢查：使用者要求的手段（X）與其目的（Y）之間，想得出更便宜的
   替代路 → 動手前用 ≤3 行提出；想不出 → 直接做，不硬掰替代案。
   本條刻意放常載而非情境載入檔：實測過，這種檢查靠情境載入自我觸發會漏。

## 路由表（遇到情境 → 讀對應檔或用 skill，再動手）

| 情境 | 去處 |
|---|---|
| 設計新模組/公開 API/資料結構，或建立新的原始碼檔（需檔頭） | 讀 `~/.claude/rules-lib/code-craft.md` |
| 準備向使用者回報（完成/卡住/提問） | 讀 `~/.claude/rules-lib/reporting.md` |
| 要派 subagent、要寫交辦 prompt，或要決定主對話用哪隻模型 | 讀 `~/.claude/rules-lib/dispatch.md` |
| 拿不定主意：算完成？該問人？該換路？品質夠嗎？ | 讀 `~/.claude/rules-lib/judgment.md` |
| 高風險判斷：架構決策、多方案取捨、規格模糊、難根因 | 讀 `~/.claude/rules-lib/uplift.md` 照強度分級執行 |
| 重大結論要對抗審查 | 讀 `~/.claude/rules-lib/dispatch.md` §3 |
| 準備宣稱「完成」或 commit | 用 skill `/done-check` |
| 除錯卡住、同一問題修 2 次沒好 | 用 skill `/debug-protocol` |
| 被使用者糾正 | 用 skill `/lesson` |
| 想修改 ~/.claude/ 下任何制度檔 | 先讀 `~/.claude/rules-lib/maintenance.md` |

## 制度分層（任何新規則先決定放哪層，能上不下）

| 層 | 載體 | 放什麼 |
|---|---|---|
| 0 | hooks / permissions（settings.json，用 /update-config） | 機器可判定的規則，最可靠 |
| 1 | 本檔 ＋ `~/.claude/rules/` 下無 `paths:` frontmatter 的檔（自動常載） | 每次必守、1–2 行寫得完的硬規則 |
| 2 | `~/.claude/skills/` 與 `~/.claude/rules-lib/` 情境載入檔 | 多步驟程序、checklist、範例——**觸發條件容易被任務表面「看起來單純」蓋過的檢查不能只放這層**（見起手式第 2 條） |
| 3 | 專案 `tasks/lessons.md` | 只放待升級規則；事實與偏好走 auto memory（層 4），不佔這層 |
| 4 | Claude Code auto memory（`~/.claude/projects/*/memory/`） | 只放事實與偏好，不放規則 |

條文衝突時的優先序：誠實條款（judgment.md）> hard-rules > 情境載入檔/skills > lessons.md
（hooks 是機器強制，不參與此排序）。

本制度與 harness 內建指引衝突時**不自行選邊**：回報使用者判斷。選擇覆寫內建的條文
必須在該條文旁寫明**覆寫的理由**，且該理由不得與內建的事實性陳述相牴觸——**規則可以
覆寫內建，理由不行**（矛盾的理由會讓模型在衝突時任意選邊，比刪掉規則更糟）。
內建**行為層**與規則對撞時（不只是理由過期），一律回報使用者重新裁定，不自行沿用舊規則。

## 常載規則

`~/.claude/rules/` 下無 `paths:` frontmatter 的檔（`hard-rules.md`、`code-standards.md`）
由 Claude Code 自動常載，不需 `@import`。變更歷史一律在 git 與 repo 的 `CHANGELOG.md`。
