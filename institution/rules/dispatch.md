# 模型調度守則

<!-- 按需引用檔。交辦任何 subagent 前讀本檔。建立：2026-07-05（Fable 5 session）。 -->

## 原則：指揮官不下場

主對話（指揮官）只做四件事：理解需求、拆解任務、做「換便宜模型就掉品質」的判斷、整合結論。
大量讀取、掃 repo、查網頁、批次改檔、驗證——一律派 subagent，主對話只進結論。

## 可用型號與參數（2026-07-05 查證值；來源見各行註記）

| 用途 | 值 | 來源 |
|---|---|---|
| Agent 工具 `model` 參數 | `haiku` / `sonnet` / `opus` / `fable` | 本 harness Agent 工具 schema |
| agent 定義 frontmatter | `model:`（同上，另可 `inherit` 或完整 model ID）、`effort: low\|medium\|high\|xhigh\|max` | code.claude.com/docs/en/subagents.md |
| settings.json `effortLevel` | `low` / `medium` / `high` / `xhigh` | code.claude.com/docs/en/settings.md |
| 完整 model ID | `claude-haiku-4-5-20251001`、`claude-sonnet-5`、`claude-opus-4-8`、`claude-fable-5` | harness 環境宣告 |

註：型號會過時。引用本表前若距上方日期超過約 3 個月，先派 claude-code-guide 重新查證再改本表（改法見 maintenance.md）。

## 調度表（任務 → model）

| 任務類型 | subagent / model | 理由 |
|---|---|---|
| 大範圍搜尋、掃 repo、定位程式碼 | `Explore` + `model: haiku` | 唯讀、量大、判斷淺 |
| 讀文件並摘要、查網頁、read-back 驗證 | `general-purpose` + `model: haiku` | 同上 |
| 一般實作、批次改檔、跑測試修測試 | `general-purpose` + `model: sonnet` | 執行為主，判斷中等 |
| 架構決策、難 bug 根因、審查仲裁、多答案評審 | `general-purpose` + `model: opus` | 判斷深，值得貴模型 |
| `fable` | 不派 | 額度稀缺，僅使用者明說才用 |

拿不準用哪級 → 先派便宜的，照下方升級路徑走，別直接上貴的。

## 交辦三要素（缺一不發）

1. **目標與動機**：做什麼＋為什麼（讓 subagent 能自行取捨細節）。
2. **驗收條件**：可驗證的完成判準（能寫成指令最好）。
3. **回報格式**：指定長度上限與結構。

範本直接抄 `~/.claude/rules/prompt-templates.md`，不要即興寫。

## 回報合約（寫進每個交辦 prompt）

- 只回結論與「檔案:行號」，不貼大段原文。
- 長產物（報告、程式碼、清單）存檔到指定路徑，回報只給路徑＋3 行摘要。
- 明確寫「查不到就說查不到，禁止編造」。

## 升降級路徑

- **haiku 錯 1 次** → 同任務升 sonnet 重派（附 haiku 的錯誤輸出當反例）。
- **sonnet 同一子任務連錯 2 次** → 升 opus，交辦時附完整失敗軌跡（兩次的輸入、輸出、錯在哪）。
- **opus 解出模式後** → 把解法寫成明確步驟，降回 sonnet/haiku 批次套用到其餘同類項。
- **同一子任務的「交辦」最多重試 2 輪**（升級也算輪）：仍失敗 → 停，向使用者回報事實、
  已排除假設、卡點。
- 層級區分（別跟除錯搞混）：本節的「輪」指指揮官重新交辦 subagent 的次數；
  hard-rules #6 與 /debug-protocol 的「3 次」指單一 agent 在自己 context 內的除錯修改次數。
  兩者各自計數，互不抵扣。

## 驗證（不自驗）

修改者永不擔任自己產出的唯一驗證者。驗證一律派 **fresh-context** agent（乾淨 context，
沒看過實作過程），並且驗證 prompt 只給規格、不給實作者的自述：

| 產出類型 | 驗證方式 |
|---|---|
| 檔案/文件 | read-back：叫它讀檔，回答「是否完整、與規格哪裡不符、哪句弱模型會誤讀」 |
| 程式碼 | 實跑：跑測試或走主流程，貼輸出；不接受「看起來正確」 |
| 高風險判斷 | 第二意見：同題派 2 個 agent 各自作答比對分歧；或多答案評審擇優 |

驗證 agent 的回報也遵守回報合約：結論 + 檔案:行號 + 修正建議，不整篇重抄。
