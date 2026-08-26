# Todo（範圍外發現，待使用者決定）

## 常載 context 還能怎麼降（2026-08-26 討論結論，待使用者選路徑）

**現況實測**（非估計，去 HTML 註解後）：

| 檔案 | 行數 | 位元組 |
|---|---|---|
| `CLAUDE.md` | 51 | 3,281 |
| `rules/hard-rules.md` | 63 | 4,395 |
| `rules/code-standards.md` | 27 | 1,513 |
| 合計 | 141 | 9,189（約 3K token） |

外加 3 個 skill ＋ 3 個 agent 的 description 與 memory 索引。2026-08-26 這輪已做兩件事：
刪掉 `prompt_nudge.sh`（原本每個 user turn 注入一次並留在對話歷史，成本隨回合數累積）、
清掉制度檔內的變更沿革（156 → 141 行，9,687 → 9,189 B）。

**核心論點：「讓模型自己判斷該載入什麼」不是沒試過，是試過會漏。**
`intake.md` 就是情境載入檔，2026-08-06 實測三次自我觸發全部失敗，所以 XY problem
判準被搬回常載起手式；本檔另記著 uplift 方法 1 在 t5 未被觸發。兩筆負面實測都指向
同一件事：情境載入的觸發判斷本身會被任務表面「看起來單純」蓋過。
**因此不建議把常載內容大幅拆成情境載入檔。**

**剩下兩條路徑，依可靠度排序：**

1. **先用 `InstructionsLoaded` hook 事件實測**（建議先做這個）。Claude Code 2.1.241 的
   hooks 已擴充到 31 個事件，其中 `InstructionsLoaded` 可記錄「這個 session 實際載入了
   哪些指令檔」。在動任何刀之前先量到真實資料，而不是繼續靠推論。
2. **給 `rules/code-standards.md` 加 `paths:` frontmatter**（機器判定，不依賴模型自律）。
   該檔只在動程式碼檔時才有意義，加上 `paths:` 可讓 Claude Code 自己決定載不載，
   省 1,513 B。等路徑 1 量到資料後再決定要不要做。

## ~~README.md「institution/agents/ 是 wshobson/agents git clone」段落過期~~（2026-08-24 已解決）

2026-08-24 實測確認 `~/.claude/agents/` 無 `.git/`，只有 3 個自製 `.md`——描述確已過期。
該段已刪除，改為註記實測結果，並補上「內建 `/code-review`／`/simplify`／`/security-review`
優先，需三個獨立 verdict 才派 agent」的使用順序。

## ~~statusline.sh 尚無檔頭~~（2026-08-24 已解決）

已依 `rules-lib/code-craft.md`（原 `code-header.md`）模板補上模組檔頭：敘述、
關鍵設計決策（為何用 POSIX sh、讀不到的欄位為何留空）、Features、已知極限
（缺 jq 時靜默降級）、Dependencies。補完後餵一份最小 JSON 實跑確認輸出正常。

## ~~restore.sh skills 迴圈硬編碼三個名字~~（2026-08-24 已解決）
已改為 `for f in "$SRC"/skills/*/SKILL.md`，與 rules/、rules-lib/、agents/ 的寫法一致。
`bash restore.sh --dry-run` 確認三個 skill 皆被列舉。

## eval/answers/t3-answer.md 行號過期（2026-08-24 回歸測試發現，未修）

答案卷寫 bug 在 `eval/fixtures/buggy_stats.py:47`，實際在 `:38`。不影響評分（判準是
「指到 `for i in range(len(levels) - 1)` 這一行」，行號只是輔助），但答案卷是評分者
唯一參考，錯的行號會讓評分者誤判。順帶檢查其他答案卷有無同類問題。

## uplift.md 方法 1「先寫判準再作答」在 t5 未被觸發（2026-08-24 觀察，暫不處理）

2026-08-24 回歸測試 t5 得 5/6，唯一失分項就是這條——規則活著、檔案完整保留、
CLAUDE.md 路由表也指向它，就是沒被觸發。與 2026-08-06 `intake.md` 的 t6 失敗同類
（情境載入檔的自我觸發判斷本身會失敗），但嚴重度低得多（t6 是整題 0/6）。
**決定：記為觀察，不因 n=1 就把它升到常載**（`maintenance.md` 加常載兩題的門檻沒過）。
第 2 次觸發再依制度分層升級。完整理由見 `eval/results/2026-08-24-opus5-精簡後.md` 結論節。

## 驗證 TaskCreate/TaskList 跨 session 持久性（2026-08-06 精簡計畫附帶發現，未修）
hard-rules #4「範圍外發現記到 tasks/todo.md」是否該改用內建 TaskCreate 尚未確定——
內建 task 系統的跨 session 持久性未查證。驗證法：建一個 task 後結束 session，
新 session 跑 `TaskList` 看是否仍在。若持久，#4 可能該搬到內建機制；若不持久，
維持現況（`tasks/todo.md` 檔案持久性是確定的）。

## ~~done-check／debug-protocol 範本未納入必填欄位~~（2026-08-24 已解決）

`done-check` 的固定回報模板已加入「已驗證:／範圍外發現:／AUTH:」三行，並註明它們是
逐字必填欄位、不適用 `reporting.md` §2 的選擇性省略。`debug-protocol` 的「修好之後」
節加一段提醒：除錯查根因時最常踩到 hard-rules #4，範圍外發現一律記 todo 不順手修。

## restore.sh 的 --prune 現在是真的痛點（2026-08-24 升級：由「長期應該」變成「下次還原前必須」）

原記於 2026-08-06：`restore.sh` 只 cp 不 rm，快照刪掉的檔不會從 `~/.claude/` 正本消失。
2026-08-24 精簡一次刪掉 `rules-lib/` 四個檔（`intake.md`、`prompt-templates.md`、
`code-header.md`、`design-heuristics.md`），還原後這四個孤兒檔仍會留在
`~/.claude/rules-lib/`——它們不進常載（不佔 token），但 CLAUDE.md 路由表已不指向它們，
且內容與新檔矛盾（例如舊 `dispatch.md` 的「一律派 subagent」）。**本次已手動 rm 處理**，
但下次改版前應該把 `--prune` 做出來：比對快照與正本、列出正本獨有的檔案供確認刪除。

## 為 4 個 hooks 補 e2e 測試（2026-08-24 新增，來自 fable-harness 比較）

`institution/hooks/` 共 1053 行（含 443 行的 `rm_guard.py`）**完全沒有測試**——repo 內
唯一的 `test_*.py` 是 eval fixture，不測 hook。對照組 `Miguok/fable-harness` 有
`tests/test_verify_gate.py` 12 案例 363 行，且每個案例都可追溯到一次真實失效
（多生態測試指令誤擋、假放行、`--test` 自測入口誤擋、內部例外仍須 fail-open）。
`rm_guard.py` 是全 repo 風險最高的檔（誤擋正常刪除／漏擋災難刪除），最該先補。
詳見 `docs/compare-fable-harness-2026-08.md` §3.1。

## 用 hook 的 prompt/agent handler 補兩個已知弱點（2026-08-24 新增）

Claude Code 2.1.241 的 hooks 已從 5 個事件擴充到 31 個，handler 除 `command` 外新增
`prompt`（LLM 判斷）與 `agent`（子代理判斷，官方標示 experimental）。這讓下方弱點
路線圖第 1 項（lesson 升級迴圈無機器強制）與第 3 項（「驗證不自驗」判不了驗證品質）
第一次有了機器強制的可能路徑。另有 `InstructionsLoaded` 事件可記錄實際載入了哪些
指令檔，正好用來驗證本制度的載入假設。**屬能力增強不是精簡，本次未做。**

## ~~README.md「檔案清單」與 institution/hooks/ 實際內容不符~~（2026-07-12 已解決）

已於本次任務一併修正：`rm_guard.py` 補進 `institution/hooks/`，README 的 hooks
（2→5 檔）、rules（9→10 檔，補 `final-assessment-fable5.md`）、memory（2→3 檔）
小節與「共 24 檔」總數（→29）皆已校正並與 `find institution -type f | wc -l`
的實算結果一致。
（註：以上檔數為 2026-07-12 當時狀態；2026-07-13 制度精簡後現為 rules 9 檔、
共 23 檔，以 README 現行清單為準。）

## ~~README.md「institution/backups/（今日 4 個 .bak）」措辭過期~~（2026-07-12 已解決）

已依使用者指示改為「2026-07-05 當日的 4 個 .bak」，不再用「今日」這種會隨時間
推移過期的相對時間詞。

## 制度剩餘已知弱點路線圖（2026-07-13 自 final-assessment-fable5.md 抽出保存；原檔已刪，全文見 git history）

按風險排序，供後繼 session 接續：

1. **lesson 升級迴圈無機器強制**：被糾正後不記 lesson 無人發現，而制度複利全靠此迴圈。
   糾正事件難以程式偵測，屬固有弱點——目前只靠使用者抽查 lessons.md。
   （原本另有 `prompt_nudge.sh` 每回合提醒，已於本次刪除：它注入的三句話全部與常載規則或
   `verify_gate` 的機器強制重複，成本卻隨回合數累積。機器強制的替代路徑見下方
   「用 hook 的 prompt/agent handler 補兩個已知弱點」。）
2. **verify_gate 已知極限**（已寫進其 docstring）：驗不了測試是否通過、雙 Stop 逃逸、
   窗口只到最後一則真人 prompt。補償：`grep BLOCK ~/.claude/hooks/hooks.log` 稽核。
3. **「驗證不自驗」只有半條機器強制**：v1.1 認得「有沒有派驗證 agent」，判不了驗證品質。
   防敷衍靠 dispatch.md 驗證 prompt 規範（不給實作者自述）。
4. **不可判定詞未給判準**：「重要交付」「非平凡修改」「重大結論」。建議判準（未入常載）：
   重要交付＝會被 commit 或交使用者驗收；非平凡＝動到 >1 檔或任何公開介面。第 2 次出錯再固化。
5. ~~小額重複（uplift 邊界節、maintenance 踩雷節）~~（2026-07-13 已於制度精簡時順手處理）。
6. **Bash 繞過 Edit 類 hook**：`sed -i` 直改制度檔不觸發 backup_gate。堵它需攔所有 Bash
   並解析語意，誤擋成本過高，判定不值得（已記載於 backup_gate docstring）。
7. **額度問題未確認**：被安全機制導向 Opus 4.8 的請求是否消耗當前窗口額度——未實測。
   確認法：claude.ai usage 儀表板，發一個會被導向的請求前後對照。確認前一律假設「所有請求都花錢」。
8. **蒸餾管道只捕錯誤、不捕平庸**（2026-07-14 Fable 5 session 盤點發現）：lessons 迴圈
   只在使用者糾正時觸發；弱模型「做得平庸但沒錯到被糾正」的靜默品質下降永遠進不了
   lessons。建議機制：趁 Fable 5 可用時，定期讓它 review 弱模型 session 的實際產出，
   把「我會這樣做而它沒有」的差距主動寫成 lesson（主動蒸餾），不等使用者發現。
   另記三項已確認的蒸餾天花板（不求解，只需知道存在）：觸發判斷本身
   （弱模型不知道自己該拿不定主意，路由表不會被錯誤的自信觸發）、長鏈推理與
   工作記憶（模型能力本體）、制度自身的演化能力（精簡與仲裁需 Fable 5 級判斷，
   已由 maintenance.md 交還使用者核准）。

## Deferred：規則准入紀律（借鑑 fable-method prime directive）

每條新規則必綁一個具名失敗案例（寫不出失敗案例的規則不加）。
使用者 2026-07-19 決定暫緩（時間成本過高）。日後重啟時的起點：
eval/cases/ 案例台帳 + maintenance.md 准入條款；現況僅 hard-rules #15 有完整
「失敗案例→規則」的完整迴圈（lessons.md 假同步教訓），可作首個範本。
