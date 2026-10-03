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
├── run.sh                    執行器：跑有制度（A）／零制度（C）並驗證條件確實不同
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

**t3–t6 用 `run.sh`**（t1／t2 區分力低，目前不跑）：在**正常終端機**（不是 Claude Code session 內）執行

```bash
bash eval/run.sh A          # 有制度：t3/t4 各 1 次、t5 2 次、t6 3 次
bash eval/run.sh C          # 零制度（--safe-mode）
```

它會預檢環境、每題開獨立沙盒（全新乾淨 context，不連續跑多題）、**prompt 直接取自任務檔**，
跑完自動檢查「制度確實載入（A）／確實未載入（C）」。手動跑時照下列原則：

1. 針對每一題，開一個**全新、乾淨 context 的 Opus session**，把該任務檔「任務 prompt」節的
   內容**逐字**貼給它（不要改寫、不要加額外提示，除非該輪評測本身就是在測別的變因）。
2. 評分者（不是受測 session 自己）對照該任務檔的「評分 checklist」逐項打 0 或 1 分。
   每一項都設計成「可觀察」，判斷不了就標「不確定」，不要硬湊分數。
3. t3、t4、t5、t6 有對應的答案卷／評分備註在 `eval/answers/`，**只給評分者看，
   絕對不能貼給受測 session**（貼了等於洩題）。
4. 結果記錄到 `eval/results/<日期>-<模型>-<條件>.md`（照 `TEMPLATE.md`）。有制度與零制度合併成一份時，
   必須有「與協定的差異」節，誠實列出樣本數、作廢的 run、評分者是誰。

## 已知陷阱（2026-10-03 第一輪 eval 全部踩到）

1. **子 session 會繼承環境變數。** 在 Claude Code session 內用 `claude -p` 啟動受測 session，
   會繼承 `CLAUDE_CODE_SAFE_MODE=1`／`CLAUDE_CODE_DISABLE_CLAUDE_MDS=1`，「有制度」組悄悄變成零制度，
   整輪作廢。判斷條件有沒有生效，**不能只看 exit code**：要看 transcript 的 skill 清單有沒有
   `verify`、上下文有沒有 `claudeMd`。`run.sh` 已內建預檢與載入檢查。
2. **`answer.md`（`claude -p` 的 stdout）只存最後一則訊息。** 有制度組會被 `verify_gate` Stop hook
   擋下一次，最後一則常變成對 hook 的補充說明，原始回報在前一則。評分一律用 transcript 裡
   **全部 assistant 文字**，且有制度與零制度要用同一種方式取。
3. **評分要盲、要同批。** 把答案換成隨機代號（對照表自己留著），有制度與零制度**放在同一批**交給同一個
   fresh-context 評分者，才沒有「前後兩個評分者標準不同」的問題。評分者只讀答案與評分檔，不讀其他檔。
4. **查證「受測 session 有沒有讀某個檔」要涵蓋所有工具。** 只搜 `Read` 工具會漏掉 `Bash cat`；
   搜 transcript 裡 `tool_use` 的完整 input。
5. **細項不確定或不適用不計分。** t6 第 4 項（提問）在答案沒提問時是 N/A；第 5 項只有條件句沒有明講
   「假設」字樣時標「不確定」。所以 t6 的實際分數上限不是 6，比較時要在同一個口徑下。

## 執行時機

**只在制度改版時跑**：新增或修改 `~/.claude/CLAUDE.md`、`rules/` 下任一常載或情境載入檔、
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
