# 工作設定

## 路由

| 情境 | 去處 |
|---|---|
| 高風險判斷：架構決策、多方案取捨、規格模糊、難根因 | 讀 `~/.claude/rules-lib/uplift.md`，照強度分級執行 |
| 除錯 | plugin skill `diagnosing-bugs`（mattpocock-skills） |
| 新功能、需求模糊 | `/grill-with-docs`；一個 session 做不完再 `/to-spec` → `/to-tickets` → `/implement` |
| 審查 | 內建 `/code-review`（正確性）、`/simplify`、`/security-review`；plugin 的 `/mattpocock-skills:code-review` 是 Standards／Spec 兩軸，撞名時明打全名 |

## 派工

預設主對話自己做完。派 subagent 的合理理由只有：中間輸出會淹沒主 context、需要 fresh-context 第二意見、使用者明講要派。

**模型選擇**（型號以當前 Agent tool schema 的 `model` enum 為準）：

| 情境 | agent 類型 | model |
|---|---|---|
| 掃 repo、位置不明的大範圍搜尋、批次讀十幾個檔 | `Explore` | `haiku` |
| 探索後要跨多處歸納結論 | `Explore` | `sonnet` |
| 規格清楚的實作、有基線測試的重構 | `general-purpose` | `sonnet` |
| 事實查證研究 | `general-purpose` | `haiku`；要權衡結論用 `sonnet` |
| 查 Claude Code／Agent SDK／API 官方行為 | `claude-code-guide` | 依該 agent 定義 |
| 設計實作策略、架構取捨 | `Plan` | `opus` |
| fresh-context 驗證 | `general-purpose` | 文件 read-back `haiku`；程式碼實跑 `sonnet` |

越唯讀、越機械就越便宜；越需要判斷就越貴。拿不準先派便宜的。

- **必明確指定 `model`**，不留空繼承。description 標明類型與模型，例：「掃描 repo（Explore+haiku）」。
- 互相獨立的任務在同一則訊息平行派出。
- plugin agent 的 description 寫「Use PROACTIVELY」只是作者的提示，不等於使用者要派。

**升降級**：
- `haiku` 錯 1 次 → 升 `sonnet`，附 haiku 的錯誤輸出當反例。
- `sonnet` 同一子任務連錯 2 次 → 升 `opus`，附完整失敗軌跡。
- `opus` 解出模式後 → 寫成明確步驟，降回 `sonnet`／`haiku` 批次套用。
- 同一子任務最多重試 2 輪（升級也算），仍失敗就停，向使用者回報事實、已排除的假設、卡點。
- 量大不等於需要升級：改 40 個檔的 import 路徑是機械活，`haiku` 批次做加抽查即可。
- `fable` 不派為 subagent，使用者明說才用。

**派工包**（目標與動機、驗收條件、回報格式缺一不發）：

```
目標與動機：<做什麼>，因為 <為什麼>。
範圍與限制：只准動 <檔案範圍>；不確定的設計決策用最簡單解並標註 ASSUMPTION。
驗收條件：<可機械判定，例如「pytest tests/x.py 全綠」>，不是「能動就好」。
回報格式：結論 ＋「檔案:行號」；長產物存到 <路徑> 後只回路徑＋3 行摘要。上限 N 行。
查不到／做不到就直說，禁止編造，禁止交出沒跑過的程式碼。
```

各類任務加一句：
- 搜尋：也查別名、舊名、字串引用；找不到回「無結果」並列出搜過的 pattern。
- 重構：列出不變式；先跑測試記錄基線再小步改；任何一步變紅且 2 次內修不回就 revert 全部並回報。
- 研究：來源優先序為官方文件 > 原始碼 > 其他；每個結論附出處；區分事實與推測；禁止用訓練記憶充當查證結果。
- 審查：審查者沒參與實作，只看規格與程式碼，不給實作者自述；回 verdict 加按嚴重度排序的問題清單。

**驗證不自驗**：修改者不當自己產出的唯一驗證者。文件用 fresh-context read-back；程式碼派 agent 實跑並貼輸出；高風險判斷同題派 2 個 agent 各自作答比對分歧。
