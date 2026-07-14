# 制度蒸餾最小評測集

## 用途

量測「Opus + 這套制度（`~/.claude/CLAUDE.md` 與 `rules/`、`skills/`）」相對於
「Opus 沒有這套制度」或「Fable」的產出品質增益，取代目前純靠主觀印象的推測值。

**這不是日常 CI，只在制度改版時跑一輪**（例如新增/修改常載規則、skill、hook 之後，
想確認有沒有實質提升或退步時）。不要把它接進每次 commit 或每日排程。

## 目錄結構

```
eval/
├── README.md                本檔
├── tasks/                    六個任務檔，每檔含「任務 prompt」「評分 checklist」「備註」
├── fixtures/                 t1~t4 用到的程式碼與測試 fixture
├── answers/                  t3~t6 的答案卷／評分備註，僅供評分者查看
└── results/                  每次評測跑完的結果記錄，含 TEMPLATE.md
```

六個任務涵蓋的能力面向：

| 任務 | 面向 |
|---|---|
| t1-implement-cli.md | 中等難度：從零實作 |
| t2-refactor.md | 中等難度：重構（行為不變、簽名不變） |
| t3-debug-logic.md | 除錯：確定性 bug（root cause + 最小修法） |
| t4-debug-intermittent.md | 除錯：間歇性 bug（不靠加 sleep/retry 掩蓋） |
| t5-architecture.md | 高難度：規格模糊的架構取捨 |
| t6-xy-problem.md | 需求端判斷：辨識 XY problem、反建議 |

## 執行方式

1. 針對每一題，開一個**全新、乾淨 context 的 Opus session**（不要在同一個 session
   連續跑多題，會有 context 汙染，也不公平——受測 session 應該像第一次遇到這個任務）。
2. 把該任務檔「任務 prompt」節的內容**逐字**貼給受測 session（不要改寫、不要加額外
   提示，除非該輪評測本身就是在測「有無制度」以外的另一個變因）。
3. 讓受測 session 完成任務。
4. 任務完成後，評分者（不是受測 session 自己）對照該任務檔的「評分 checklist」
   逐項打 0 或 1 分。checklist 每一項都設計成「可觀察」（能從回報的指令輸出、diff、
   檔案內容直接判斷），盡量不要靠印象裁量；判斷不了就標「不確定」，不要硬湊分數。
5. t3、t4、t5、t6 有對應的答案卷／評分備註在 `eval/answers/`，**只給評分者看，
   絕對不能貼給受測 session**（貼了等於洩題，t3/t4 會失去除錯任務的意義）。
6. 把結果記錄到 `eval/results/<日期>-<模型>-<有無制度>.md`，複製
   `eval/results/TEMPLATE.md` 開始填。例如：
   `eval/results/2026-07-15-opus-有制度.md`、`eval/results/2026-07-15-fable-baseline.md`。

## 執行時機

**只在制度改版時跑**：新增或修改 `~/.claude/CLAUDE.md`、`rules/` 下任一常載或按需檔、
`skills/` 下任一 skill 之後，想確認這次改動對 Opus 的實際產出品質有沒有幫助（或有沒有
意外傷害）時，才跑一輪完整的六題。不要日常化、不要接 CI，六題全跑一輪對一般任務來說
成本偏高，只有「制度本身要不要改」這種問題值得付出。

## 驗證 fixture 本身是否還正常

`eval/fixtures/` 下的 t2/t3/t4 是可執行、可驗證的：

```bash
# t2：重構前的基線應全綠
python3 -m pytest eval/fixtures/test_refactor_target.py -q

# t3：重現指令應印出錯誤值 2（正確應為 3）
cd eval/fixtures && python3 -c "from buggy_stats import longest_error_streak; print(longest_error_streak(['OK', 'ERROR', 'ERROR', 'ERROR']))"

# t4：重現腳本應在 10 輪內至少出現數次 FAIL（間歇性，不保證每次執行都一樣）
cd eval/fixtures && python3 repro_flaky_cache.py
```

如果之後改了 fixture 卻忘記重新驗證這三個指令，任務檔裡描述的「已驗證」字樣就會
變成謊言——改動 fixture 後務必重跑這三條指令確認行為符合任務檔敘述。
