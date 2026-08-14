# AI Assistant Workflow Configuration（索引）

<!-- v3.3 (2026-08-06)：依 eval 實測（t3–t6，Opus 5，A 現行制度 vs C `--safe-mode` 零制度）
     精簡——刪 @import（`~/.claude/rules/` 下無 paths frontmatter 的檔本已自動常載）、
     刪 hard-rules #14／計畫節第 1 條（內建 harness 已覆蓋）、XY problem 核心判準搬進
     起手式常載（`intake.md` 按需觸發實測三次全部失敗，機制不可靠而非內容問題）、
     新增與內建衝突時的處理原則。常載上限 500→200 行（對齊官方建議）。
     完整實測數據與逐條比對見 docs/harness-overlap-2026-08.md（使用者核准）。
     v3.2 (2026-07-15)：分層表下新增條文衝突優先序一行（蒸餾計畫 P2，使用者核准）。
     v3.1 (2026-07-14)：路由表新增 intake / design-heuristics / reporting 三行
     （Fable 5 session 補蒸餾，使用者核准）。
     v3.0 (2026-07-05)：本檔只當索引路由，≤150 行。新增內容一律寫新檔再在此加一行
     路由，不塞長內容進本檔。歷史版本在 ~/.claude/backups/。
     維護規約見 ~/.claude/rules-lib/maintenance.md。 -->

## Session 起手式

1. 動手前一句話複述：任務範圍 + 完成判準。只有「走錯方向的代價 > 提問成本」才提問，
   否則寫下假設繼續做。
2. XY problem 快速檢查：使用者要求的手段（X）與其目的（Y）之間，想得出更便宜的
   替代路 → 動手前用 ≤3 行提出；想不出 → 直接做，不硬掰替代案。
   （2026-08-06 實測：這條靠按需檔 `intake.md` 自我觸發不可靠——同一失敗模式三次
   獨立測試全部複現，包括理論上會讀到 `intake.md` 的情境，故把核心判準搬進本常載
   起手式；`intake.md` 保留完整版含正反例、與本條互補的 scope 校準檢查。）

## 路由表（遇到情境 → 讀對應檔或用 skill，再動手）

| 情境 | 去處 |
|---|---|
| scope 落差校準、需要 XY problem 正反例（快速版已在起手式） | 讀 `~/.claude/rules-lib/intake.md` |
| 要設計新模組、公開 API、資料結構 | 讀 `~/.claude/rules-lib/design-heuristics.md` |
| 準備向使用者回報（完成/卡住/提問） | 讀 `~/.claude/rules-lib/reporting.md` |
| 中間輸出會淹沒主對話、或需要 fresh-context 第二意見 | 讀 `~/.claude/rules-lib/dispatch.md` |
| 寫交辦 prompt（搜尋/實作/重構/研究/審查） | 抄 `~/.claude/rules-lib/prompt-templates.md` |
| 拿不定主意：算完成？該問人？該換路？品質夠嗎？ | 讀 `~/.claude/rules-lib/judgment.md` |
| 高風險判斷：架構決策、多方案取捨、規格模糊、難根因 | 讀 `~/.claude/rules-lib/uplift.md` 照強度分級執行 |
| 建立新的原始碼檔案（需模組敘述檔頭） | 讀 `~/.claude/rules-lib/code-header.md` |
| 準備宣稱「完成」或 commit | 用 skill `/done-check` |
| 除錯卡住、同一問題修 2 次沒好 | 用 skill `/debug-protocol` |
| 被使用者糾正 | 用 skill `/lesson` |
| 想修改 ~/.claude/ 下任何制度檔 | 先讀 `~/.claude/rules-lib/maintenance.md` |

## 制度分層（任何新規則先決定放哪層，能上不下）

| 層 | 載體 | 放什麼 |
|---|---|---|
| 0 | hooks / permissions（settings.json，用 /update-config） | 機器可判定的規則，最可靠 |
| 1 | 本檔 ＋ `~/.claude/rules/` 下無 `paths:` frontmatter 的檔（自動常載） | 每次必守、1–2 行寫得完的硬規則 |
| 2 | `~/.claude/skills/` 與 `~/.claude/rules-lib/` 按需檔 | 多步驟程序、checklist、範例——**觸發條件容易被任務表面「看起來單純」蓋過的檢查不能只放這層**（2026-08-06 intake.md 實測教訓，見起手式第 2 條） |
| 3 | 專案 `tasks/lessons.md` | 只放待升級規則；事實與偏好走 auto memory（層 4），不佔這層 |
| 4 | Claude Code auto memory（`~/.claude/projects/*/memory/`） | 只放事實與偏好，不放規則 |

條文衝突時的優先序：誠實條款（judgment.md）> hard-rules > 按需檔/skills > lessons.md
（hooks 是機器強制，不參與此排序）。

本制度與 harness 內建指引衝突時**不自行選邊**：回報使用者判斷。選擇覆寫內建的條文
（例如 hard-rules #11），必須在該條文旁寫明**覆寫的理由**，且該理由不得與內建的
事實性陳述相牴觸——**規則可以覆寫內建，理由不行**（矛盾的理由會讓模型在衝突時
任意選邊，比刪掉規則更糟；見 hard-rules #11 的實例）。

## 常載規則

`~/.claude/rules/` 下無 `paths:` frontmatter 的檔（`hard-rules.md`、`code-standards.md`）
由 Claude Code 自動常載，不需 `@import`。
