# t3 — 除錯（確定性）：最長連續 ERROR 統計錯誤 (中等 / 除錯)

## 任務 prompt

```
`eval/fixtures/buggy_stats.py` 裡的 `longest_error_streak(levels)` 應該回傳一份
日誌等級序列中「最長連續 ERROR」的長度，但目前算出來的值不對。

重現指令（在 repo 根目錄執行）：
cd eval/fixtures && python3 -c "from buggy_stats import longest_error_streak; print(longest_error_streak(['OK', 'ERROR', 'ERROR', 'ERROR']))"

這組輸入的正確答案應該是 3，但目前會印出別的值。請找出根因、用最小的修改修好它，
不要動測試以外的行為，也不要重寫整個函式。

完成後告訴我：根因是什麼（檔案:行號）、你怎麼修的、重現指令修好後印出的值。
```

## 評分 checklist

- [ ] 指出的根因位置為 `eval/fixtures/buggy_stats.py` 的 `longest_error_streak` 函式中
      `for i in range(len(levels) - 1)` 這一行（off-by-one：少跑最後一個索引）
- [ ] 根因描述抓到「迴圈邊界少了最後一個元素」這個本質，不是隨便猜一個看似有關的原因
- [ ] 修法是把 `range(len(levels) - 1)` 改成 `range(len(levels))`（或等價的正確邊界修法）
- [ ] `git diff` 或等價比對顯示改動 ≤10 行（實際上應該只需改 1 行）
- [ ] 修完後重新執行重現指令，印出值為 `3`（回報附實際指令輸出，不是「應該對了」）
- [ ] 沒有動到 `error_rate` 函式或其他無關程式碼

## 備註

- fixture 路徑：`eval/fixtures/buggy_stats.py`。
- 答案卷（僅供評分者查看，受測 session 不可讀）：`eval/answers/t3-answer.md`。
- 已驗證重現指令在修 bug 前印出 `2`（錯誤值），預期正確值為 `3`。
