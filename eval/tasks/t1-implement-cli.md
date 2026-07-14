# t1 — 從零實作：log 錯誤統計 CLI（中等 / 實作）

## 任務 prompt

```
請用 Python 寫一個小型 CLI 工具 `log_stats.py`，功能是統計一份 log 檔裡各等級
（INFO / WARN / ERROR）的出現次數，並印出摘要。

規格：
- log 檔每行格式為 `<ISO8601 時間戳> <LEVEL> <訊息>`，例如：
  `2026-07-15T10:00:01 ERROR disk full`
  `2026-07-15T10:00:02 INFO  startup complete`
- LEVEL 只會是 INFO / WARN / ERROR 三種之一（欄位間以任意數量空白分隔）。
- CLI 用法：`python3 log_stats.py <log 檔路徑>`。
- 印出格式（純文字，每行一項，依 INFO/WARN/ERROR 固定順序）：
  ```
  INFO: <count>
  WARN: <count>
  ERROR: <count>
  TOTAL: <count>
  ```
- 空檔案（0 行）視為合法輸入，全部欄位印 0。
- 遇到不符合格式的行：略過該行並繼續處理其餘行，不要讓程式整個中斷。
- 請一併寫 pytest 測試，涵蓋正常檔案、空檔案、含不符合格式行的檔案至少三種情況。

完成後告訴我你的驗證方式與實際跑出的結果。
```

## 評分 checklist

- [ ] `python3 -m pytest <測試檔> -q` 全綠，回報中附實際指令與輸出（不是「應該會過」）
- [ ] 回報附至少一次 CLI 實跑輸出（例如對一個手造的樣本 log 檔跑過一次，貼出印出的摘要）
- [ ] `log_stats.py`（與任何新建的 .py 檔）具備標準檔頭（File/Author/Created Date/Version/Description/...，見
      `~/.claude/rules/code-header.md` 模板）
- [ ] 程式碼與測試中無殘留除錯碼（`print` 除錯輸出、註解掉的程式碼、`pdb` 等）
- [ ] 空檔案與格式不符的行有被測試覆蓋，且行為符合規格（略過壞行、不中斷）
- [ ] CLI 輸出順序固定為 INFO/WARN/ERROR/TOTAL，且測試有斷言確切文字格式（不是只斷言「有跑」）

## 備註

- 不提供 fixture；受測 session 需自行建立測試用 log 檔（可用暫存檔或 pytest tmp_path fixture）。
- 這題沒有標準答案檔（不是 debug 題），checklist 全部是「可觀察的產出品質」判準。
