# t3 答案卷（僅供評分者查看，受測 session 不可讀）

## Bug 位置

`eval/fixtures/buggy_stats.py:47`（`longest_error_streak` 函式內的 for 迴圈行）：

```python
for i in range(len(levels) - 1):
```

## 根因

Off-by-one：迴圈邊界少算了最後一個索引。`range(len(levels) - 1)` 只走訪
`0 .. len(levels) - 2`，序列最後一個元素永遠不會被檢查到。若最長的連續 ERROR
恰好延伸到序列尾端（如 `['OK', 'ERROR', 'ERROR', 'ERROR']`），最後一個 `ERROR`
被漏算，導致回傳值比正確答案少 1。

## 建議修法

把邊界改成涵蓋整個序列：

```python
for i in range(len(levels)):
```

diff 僅 1 行。不需要改動 `error_rate` 或其他任何程式碼。

## 驗證

修法前重現指令：
```
cd eval/fixtures && python3 -c "from buggy_stats import longest_error_streak; print(longest_error_streak(['OK', 'ERROR', 'ERROR', 'ERROR']))"
```
輸出 `2`（錯誤，正確應為 `3`）。

修法後同一指令應輸出 `3`。
