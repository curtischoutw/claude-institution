# Harness 重疊覆核：2026-08-06

<!-- 目的：下次 Claude Code 大版本更新後，不必重新考古——直接重跑這張表，
     只需要更新「內建原文出處」那欄是否還成立。
     產出於 branch refactor/harness-overlap-slim；使用者核准後套用。 -->

## 為什麼做這次覆核

這套制度建立於 2026-07-05，當時 harness 的內建 system prompt 遠比現在單薄。
10 個月後，Claude Code（本次覆核時 `2.1.221`）大幅擴充了內建行為——plan mode、
TaskCreate、auto memory、Delivering work 章節、Agent tool 的使用指引等。制度裡
有些規則因此變成：(a) 內建已覆蓋的重複、(b) 規則仍成立但**理由**已被平台反轉、
或 (c) 機制設計上該生效卻實測不生效。三種問題需要三種不同的處理，不能都當成
「刪或留」的二元選擇。

## 判定分類

| 判定 | 意思 | 處理方式 |
|---|---|---|
| **刪（內建已覆蓋）** | harness 內建行為與規則完全重疊，規則變純冗餘 | 從常載/按需檔移除 |
| **留（內建無等價）** | harness 完全沒有對應機制 | 不動 |
| **降層** | 內容仍有價值，但常載成本過高 | 從常載降到按需檔/skill |
| **留規則改動機** | 規則行為仍該做，但論證理由已被平台反轉 | 規則不動，只換理由 |
| **機制修正**（本次新增，t6 實測發現） | 規則內容沒問題，但「按需觸發」依賴模型自我判斷，這個判斷本身會失敗 | 核心判準搬進常載，按需檔留完整版 |

## 逐條比對表

| 規則／檔案 | 內建原文出處 | 判定 | 處理 |
|---|---|---|---|
| hard-rules #1「沒讀過的檔案不准改」 | Edit tool 描述：「You must Read the file in this conversation before editing, or the call will fail」 | 刪（機器已強制） | 壓成「小改用 Edit，不整檔重寫」 |
| hard-rules #9「制度檔先備份」細節 | `backup_gate.py`（層 0 hook，本專案自己的機制，非 harness 內建，但已機器強制） | 刪（本地機器已強制） | 壓成一行指向 hook＋maintenance.md |
| hard-rules #14「回報結論先行」 | 本 session system prompt「Report outcomes faithfully」＋ Delivering work 節 | 刪 | 降為按需，`reporting.md` §1 是完整正本 |
| hard-rules「計畫」節第 1 條（3 步以上進 plan mode） | `EnterPlanMode` 工具描述本身即是此機制；`TaskCreate`/`TaskList` 是 todo 機制 | 刪 | 保留第 2 條（假設/風險/判準格式，內建無此要求） |
| hard-rules Git 紀律「不 commit 除錯碼」「未經要求不 commit/push」 | 本 session system prompt 明文＋`commit_guard.py` 已機器強制 | 刪 | 壓成 1 行，只留原子 commit 格式要求 |
| `~/.claude/CLAUDE.md` 的 `@import` 兩行 | 官方 memory 文件：「Rules without a `paths` field are loaded unconditionally」 | 刪（冗餘） | 移除，改一行說明自動常載 |
| CLAUDE.md 起手式「讀 tasks/lessons.md」 | 官方 memory 文件：auto memory 的 `MEMORY.md` 每 session 自動載入 | 刪 | 移除 |
| CLAUDE.md 起手式「≤5 題一次問完」 | 本 session system prompt「Reserve blocking questions...」「ask your question... at the right time」 | 刪 | 移除（XY problem 判準保留，見下） |
| `judgment.md` §3「何時問人」判準 | 本 session system prompt「Delivering work」整節 | 刪 | 保留該節後半「AUTH: 使用者說『<原話>』」必填欄位（內建無逐字產物要求） |
| `judgment.md` §1「何時升級模型」 | 與 `dispatch.md` 升降級路徑重複（非 harness 內建，是本檔自身重複） | 刪（內部重複） | 反例併入 dispatch.md |
| `diagnosis.md` 全檔 | 純指標檔，功能被 CLAUDE.md 路由表取代；獨有規則見下 | 刪 | 「加常載規則前必答兩題」併入 maintenance.md |
| hard-rules #11「一律派 subagent」（省額度理由） | Agent tool 描述：「Do not spawn agents unless the user asks... it's the expensive path on this plan」 | **留規則改動機** | 規則不動，理由換成「主 context 乾淨、避免失焦」（同一 Agent tool 描述也說 subagent 適用於「would flood the main conversation with intermediate results」） |
| `dispatch.md`「原則」節（同一過期理由） | 同上 | 留規則改動機 | 同步換動機 |
| README.md 痛點 3「額度燒在粗活」 | 同上 | 留規則改動機 | 改為「主 context 燒在粗活」 |
| `dispatch.md` 調度表（任務→model 靜態對照） | hard-rules #8「不憑記憶填」＋本檔自己 2026-07-13 已因同理由刪過型號參數表 | 刪（會過期的事實表） | 壓成「可用型號」節裡兩行原則 |
| `dispatch.md` Fable 窄閥／起手詳細規則 | 無直接內建對應；純粹是使用頻率考量 | 降層 | 壓成升降級路徑最後一條，罕見情境現場判斷 |
| `prompt-templates.md` 各範本重複的「禁止編造/回報上限」 | 檔頭「通用鐵則」節已聲明同一件事 | 刪（內部重複） | 移除各範本內重複字句，保留數字 |
| `maintenance.md` 精簡門檻「常載合計 500 行」 | 官方文件：「target under 200 lines per CLAUDE.md file」 | 降層（門檻本身無依據） | 500→200 |
| **`intake.md`「動手前查 XY problem」** | 無內建等價；問題不在內建，在本檔自己的**觸發機制** | **機制修正**（見下方「t6 實測」節） | 核心判準搬進 CLAUDE.md 常載起手式；`intake.md` 保留完整版（scope 校準＋正反例） |
| `code-standards.md` 標準檔頭要求 | 本 session system prompt：「Write code that reads like the surrounding code: match its comment density, naming, and idiom」 | **留（2026-08-06 決定不解決）→ 2026-08-14 改版後張力減輕** | 見下方「2026-08-14 檔頭改版」節 |
| hard-rules #2/#5/#6/#7/#15、`uplift.md`、`code-header.md`、`design-heuristics.md`、5 個 hooks、3 個 skills | 內建無等價（逐一核對本 session system prompt，無對應機制） | 留 | 不動 |

## t6 實測：`intake.md` 按需觸發機制失效（2026-08-06）

用 `eval/tasks/t6-xy-problem.md` 對照 A（現行制度）與 C（`--safe-mode` 零制度）
跑了三次（A×2、C×1）。三次全部 0/6——包括理論上會讀到 `intake.md` 的 A 組
兩次都複現同一失敗：直接把「用 regex 寫」的字面要求做完，沒發現資料本身是
JSON Lines。r2 甚至講到「json.loads」這個詞，卻沒連結到「現在這份資料就已經是
JSON」。

**結論**：不是規則內容問題（`intake.md` 的判準寫得很清楚），是「按需檔要靠模型
自己判斷『這個任務該不該觸發路由』」這個前置判斷本身會失敗——表面看起來單純的
請求最不容易觸發自我檢查，而這正是 XY problem 最常見的偽裝方式。完整結果見
`eval/results/2026-08-06-opus5-{有制度,零制度}.md`；教訓已記入 `tasks/lessons.md`
（2026-08-06 條目「按需觸發的規則靠模型自我判斷...」）。

## 完整實測結果摘要（t3–t6，Opus 5，A vs C）

| 題 | A 現行制度 | C 零制度 | 結論 |
|---|---|---|---|
| t3 確定性 bug | 6/6 | 6/6 | 無差異 |
| t4 間歇性 bug | 6/6 | 6/6 | 無差異 |
| t5 架構取捨 | ~4/6 | ~1/6 | 制度有實質幫助 |
| t6 XY problem | 0/6、0/6 | 0/6 | 制度未發揮作用（機制問題） |

## 2026-08-14 檔頭改版（上表「標準檔頭要求」一列的後續）

2026-08-06 這格記為「張力不解決，使用者決定保留現況」。2026-08-14 使用者重新檢視後
改版：檔頭砍掉 `File`／`Author`／`Email`／`Created Date`／`Version`／`Copyright`／
`Version History` 七個元資料欄位，只留敘述、`Features`、`已知極限`、`Dependencies`
（詳見 `CHANGELOG.md` 與 `institution/rules-lib/code-header.md`）。

**與內建的張力因此減輕**：剩下的內容就是各語言正常的 module docstring 用法，
和「reads like the surrounding code」不再直接對撞——原本最違和的是那七行
署名／版號／變更歷史，在別人的 repo 裡明顯突兀，砍掉後檔頭本身不再是異物。

**但張力沒有完全消失，也沒有新增例外條文**（使用者 2026-08-14 明確決定不加
「外部 repo 入境隨俗」規則）：在一個慣例是「完全不寫 module docstring」的外部 repo，
本制度仍會要求寫。這一格維持**留**，覆核時重新評估。

**改版的主要理由不是這個張力，而是分歧**：元資料欄位與 git 是兩份紀錄，本 repo
11 個原始碼檔已實測出 3 個版本欄位失真、11 個 `Email` 未填。理由與證據見
`institution/rules/code-standards.md` 的 Changelog 與 `CHANGELOG.md`。

## 下次覆核時怎麼用這份文件

1. 對照本表「內建原文出處」欄，跑一次等價的官方文件查證（用 WebFetch／WebSearch，
   不要憑記憶）——確認引文是否還成立、是否有新增的內建機制。
2. 任何一格「內建原文出處」不成立了 → 該規則的判定可能要重新跑一輪，不要只改
   這張表就當作已處理。
3. 「機制修正」類的規則（目前只有 `intake.md` 一條）需要**實測**才能判斷是否
   真的解決，不能只憑推論——比照 t6 的實驗設計（`eval/tasks/`＋A/C 對照）重跑。
4. 新發現的重疊或衝突，記入 `tasks/lessons.md`，第 2 次觸發依 `maintenance.md`
   權限分級走升級流程。
