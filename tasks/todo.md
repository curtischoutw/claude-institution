# Todo（範圍外發現，待使用者決定）

## README.md「institution/agents/ 是 wshobson/agents git clone」段落疑似過期（2026-08-18 三邊對齊發現，未修）

README.md ~139 行稱 `~/.claude/agents/` 是第三方 `wshobson/agents` 的 git clone，
三個制度 agent 檔名靠 `.git/info/exclude` 藏起來避免污染 git status。三邊對齊
session 實測該目錄**沒有 `.git/`**，只有 3 個自製 md。需複查這段描述是否仍成立，
不成立則改寫或刪除。

## statusline.sh 補入快照後尚無檔頭（2026-08-18 三邊對齊發現，未修）

`institution/statusline.sh`／`~/.claude/statusline.sh` 依現行 `code-header.md`
規範該有模組敘述檔頭（這個檔是什麼、為什麼存在、關鍵設計決策、已知極限），
目前完全沒有。屬修改正本內容，超出三邊對齊 session 的範圍，記於此待後續補上。

## restore.sh 加 `--prune`（2026-08-06 精簡計畫附帶發現，未修）
`restore.sh` 只 cp 不 rm——快照刪掉的檔不會從 `~/.claude/` 正本消失，會變成
「路由表沒指向但仍存在」的孤兒檔。目前靠 Phase 6 手動 `rm` 處理，長期應該讓
`restore.sh --prune` 自動比對快照與正本、列出正本獨有的檔案供確認刪除。

## restore.sh skills 迴圈硬編碼三個名字（2026-08-18 三邊對齊發現，未修）
`restore.sh` 還原 skills 的迴圈是 `for skill in done-check lesson debug-protocol`
寫死三個名字，`institution/skills/` 新增 skill 不會被自動涵蓋，需同步改腳本。
應改成掃 `$SRC/skills/*/SKILL.md` 動態列舉，與 rules/、rules-lib/、agents/ 的
迴圈寫法一致。

## 驗證 TaskCreate/TaskList 跨 session 持久性（2026-08-06 精簡計畫附帶發現，未修）
hard-rules #4「範圍外發現記到 tasks/todo.md」是否該改用內建 TaskCreate 尚未確定——
內建 task 系統的跨 session 持久性未查證。驗證法：建一個 task 後結束 session，
新 session 跑 `TaskList` 看是否仍在。若持久，#4 可能該搬到內建機制；若不持久，
維持現況（`tasks/todo.md` 檔案持久性是確定的）。

## done-check／debug-protocol skill 範本未納入新增必填欄位（2026-07-19 發現，未修）

`feat/mandatory-artifacts` branch 給 hard-rules #3/#4 與 judgment.md 加了「已驗證:」
「範圍外發現:」「AUTH:」三個決策點必填欄位。fresh-context read-back（haiku）指出：
`skills/done-check/SKILL.md` 的完成報告範本、`skills/debug-protocol/SKILL.md` 的
假設日誌範本，都還沒把這三行納入，執行這兩個 skill 時可能遺漏。屬範圍外問題
（超出使用者核准的「3 條規則、2 檔」範圍），記錄於此，是否要一併補上待使用者決定。

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
   糾正事件難以程式偵測，屬固有弱點——靠 prompt_nudge 提醒＋使用者抽查 lessons.md。
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
使用者 2026-07-19 決定暫緩（時間成本過高）。日後重啟時的落地基礎：
eval/cases/ 案例台帳 + maintenance.md 准入條款；現況僅 hard-rules #15 有完整
「失敗案例→規則」閉環（lessons.md 假同步教訓），可作首個範本。
