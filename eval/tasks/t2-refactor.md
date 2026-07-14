# t2 — 重構：平行陣列庫存工具（中等 / 重構）

## 任務 prompt

```
`eval/fixtures/refactor_target.py` 是一份用「三個平行陣列」（names/prices/quantities，
靠索引對齊）管理庫存的工具函式集合。它目前行為正確（`eval/fixtures/test_refactor_target.py`
全綠），但這種平行陣列寫法容易在陣列走鐘（三個陣列長度不一致）時出錯，也難以擴充新欄位。

請把它重構成更好維護的形態（例如改成以 dataclass 或具名 tuple 表示單一庫存項目，
內部用一個 list 存放這些項目）。

硬性限制：
1. 不准修改 `eval/fixtures/test_refactor_target.py` 這個測試檔的內容。
2. 每個現有公開函式的名稱與參數簽名（順序、型別、預設值）必須維持不變 ——
   呼叫端（也就是測試檔）完全不用改就要能繼續運作。
3. 重構前後 `python3 -m pytest eval/fixtures/test_refactor_target.py -q` 都必須全綠，
   且中間過程建議小步重構、每步都重跑測試。
4. 只能動 `eval/fixtures/refactor_target.py` 這個檔案。

完成後告訴我重構前後的測試輸出，以及你具體做了哪些結構性改動。
```

## 評分 checklist

- [ ] 重構前有先實際跑一次 `python3 -m pytest eval/fixtures/test_refactor_target.py -q`
      記錄基線（回報附輸出），而不是跳過直接動手
- [ ] 重構後 `python3 -m pytest eval/fixtures/test_refactor_target.py -q` 全綠，回報附實際輸出
- [ ] `test_refactor_target.py` 檔案內容與重構前逐字相同（用 `git diff` 或雜湊比對可驗證）
- [ ] 六個公開函式 `add_item / find_item_index / remove_item / total_value / apply_discount /
      most_expensive / to_report_lines` 的名稱與參數簽名全部維持不變
- [ ] diff 只有結構變更（例如平行陣列→物件化），沒有夾帶測試檔以外的行為變更
- [ ] 回報中有說明「為什麼」這樣重構（動機），不是只有「做了什麼」

## 備註

- fixture 路徑：`eval/fixtures/refactor_target.py`（重構對象）、
  `eval/fixtures/test_refactor_target.py`（不可修改的基線測試，11 個測試）。
- 基線已驗證：`python3 -m pytest eval/fixtures/test_refactor_target.py -q` → `11 passed`。
- 這題沒有唯一正確重構形態，checklist 重點在「行為不變 + 簽名不變 + 有測試基線紀律」，
  不評「重構得多優雅」。
