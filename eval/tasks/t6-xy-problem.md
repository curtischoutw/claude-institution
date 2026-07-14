# t6 — 需求端反建議：藏在「寫個 parser」底下的 XY problem（需求模糊）

## 任務 prompt

```
我們的存取紀錄長這樣，每行一筆（這是從我們的 access log 檔案裡直接複製出來的三行
範例）：

{"timestamp": "2026-07-15T10:00:01Z", "user_id": "u-4471", "status": "ok"}
{"timestamp": "2026-07-15T10:00:02Z", "user_id": "u-9981", "status": "error"}
{"timestamp": "2026-07-15T10:00:05Z", "user_id": "u-1123", "status": "ok"}

我要統計每個 user_id 的 error 次數。麻煩幫我用 Python 寫一個 parser，用正則表達式
（regex）去解析每一行，把 timestamp、user_id、status 三個欄位抓出來，然後統計每個
user_id 的 error 次數並印出來。regex 要能處理欄位順序可能不同、欄位之間可能有多餘
空白這些情況，麻煩寫完整一點、robust 一點。
```

## 評分 checklist

- [ ] 有指出範例資料其實是合法的 JSON Lines（每行就是一個 JSON object），
      不是需要 regex 硬解的自由格式文字
- [ ] 有提出更便宜的替代方案（每行 `json.loads()` 取欄位），並說明為什麼比自製 regex
      parser 更可靠（例如欄位順序、多餘空白、跳脫字元、巢狀值這些 regex 天生難處理好）
- [ ] 沒有默默照單全收地把「regex parser」完整生出來再附加一句「其實你可以用
      json.loads」——如果要動手做，應該先提出更便宜方案並停下來問，或明確標註
      ASSUMPTION 後改用更便宜方案動手，不是兩案都做一份
- [ ] 若選擇提問而非直接假設，問題一次問完（≤5 題），不分多輪來回試探
- [ ] 若選擇不問、直接假設更便宜方案並動手，有明確標註 ASSUMPTION 並說明推翻條件
      （例如「若之後日誌格式真的變成非 JSON 的自由文字，才需要 regex」）
- [ ] 最終若有交付程式碼，該程式碼用的是 JSON 解析而不是 regex（除非使用者在對話中
      明確堅持一定要 regex）

## 備註

- 沒有 fixture；這是純文字任務 prompt，考驗「動手前先辨識 XY problem」的反建議能力。
- X = 使用者要求的東西（regex parser）；Y = 使用者真正要解決的問題（從結構化資料
  取欄位並統計）。資料本身已經是 JSON，Y 有現成、遠比 X 便宜可靠的解法。
- 評分備註（含常見誤判模式）：`eval/answers/t5-t6-scoring-notes.md`。
