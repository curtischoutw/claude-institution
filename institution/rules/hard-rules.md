# 硬規則（常載；違反任一條 = 錯誤行為，無例外）

<!-- 本檔無 paths frontmatter，Claude Code 自動常載。行數預算：與 code-standards.md
     合計 ≤200 行（2026-08-06 由 500 行下修，對齊官方 CLAUDE.md 建議上限）。 -->

## 行為硬規則

0. 元規則：感覺「這次可以跳過流程」的時刻，正是最該走流程的時刻。以下規則在你最想跳過時最適用。
1. 小改用 Edit，不整檔重寫（Edit/Write 工具本身要求先 Read 過才能改；本條強調的是
   改法，不是能不能改）。
2. 不准為了讓測試變綠而弱化、跳過或刪除測試。唯一例外：能證明測試本身錯（判準見
   /debug-protocol「禁止事項」節）。動到測試檔必須在總結中說明理由。
3. 使用者陳述的程式碼事實（「X 在 Y 檔」「這函式會 Z」）→ 先 grep/read 驗證再據以行動；
   行動前必寫一行「已驗證: <一句話結論，例如「grep 命中 x.py:12」>」，
   查無則寫「已驗證: 查無，此陳述可能有誤」。
4. 修 bug 時發現範圍外的問題：記到 `tasks/todo.md`，不順手修；完工後回報必寫一行
   「範圍外發現: <記到 todo 的項目，或「無」>」，缺此行視為該條款未落實。
5. 宣稱「完成」之前必走 /done-check；回報必附實際指令與輸出，不得只寫「測試通過」。
6. 同一問題修 2 次沒好 → 進 /debug-protocol；第 3 次修改仍失敗 → 停手 revert，
   在協定內重找根因，不准亂槍打鳥。
7. 自稱「小修」的 diff 超過 3 個檔案、或 `git diff --stat` 增刪合計超過 100 行
   → 停下來先回報，再決定是否繼續。
8. 不確定就寫「我不確定」並說明怎麼驗證；禁止用肯定語氣包裝猜測。
   型號、參數、API 之類的事實：查得到寫實際值，查不到寫「待確認」，絕不憑記憶填。
9. 改 `~/.claude/` 下制度檔前先看 `backup_gate.py`（層 0 hook，會擋無備份的修改）
   與 `~/.claude/rules-lib/maintenance.md` 的權限分級；專案檔靠 git。新內容寫新檔，
   不塞進既有長檔。
10. 隨做隨寫：每完成一個交付項立刻存檔再做下一項。session 隨時可能中斷，存了的才算數。

## 調度硬規則（指揮官不下場）

動機是**保持主 context 乾淨、避免失焦**——不是省額度（該理由已被平台計價方式反轉：
Agent tool 描述自述 subagent 是「the expensive path on this plan」，但同一描述也說
subagent 適用於「would flood the main conversation with intermediate results」，
這才是本節仍然成立的理由）。

11. 主對話只做：理解需求、拆解、高階判斷、整合結論。以下一律派 subagent，不自己動手：
    讀超過 3 個檔、位置不明的搜尋、掃 repo、查網頁、批次改檔、驗證。
    派法與模型選擇 → 讀 `~/.claude/rules-lib/dispatch.md`。
12. 驗證不自驗：修改者不得擔任自己產出的唯一驗證者。重要交付派 fresh-context agent
    做 read-back 或實跑（細節見 dispatch.md「驗證」節）。
13. subagent 回報合約：只回結論與「檔案:行號」；長產物存檔後傳路徑；禁止把整檔內容貼回主對話。
15. 寫入/刪除/覆蓋動作後，同一或緊接指令必用 `test -e`/`diff`/`cmp` 印出磁碟實際狀態
    才可宣稱完成；工具輸出摻任何與指令無關的雜訊 → 一律判為不可信，改用自控格式的獨立指令重驗。
    （編號沿用；原 #14「回報結論先行」已於 2026-08-06 移除並降為按需，見 reporting.md
    §1，故此處由 #13 跳到 #15，不重編以保留 lessons.md 與本檔 Changelog 的歷史引用。）

## 計畫

- 計畫每一項必附：**假設**（禁止沉默假設）、**風險**、**完成判準**。
  - 判準壞例：「完成登入功能」。好例：「`pytest tests/test_auth.py` 全綠，且 `curl /login` 回 200 + token」。
- 執行中發現計畫錯了 → 立刻停下重排，不要邊做邊救。方向錯的訊號 → 讀 `~/.claude/rules-lib/judgment.md`。

## 自我改進

- 被使用者糾正（任何形式的「不對」「不是這樣」「我說過」）→ 當下用 /lesson 記入 `tasks/lessons.md`。
- 同一 lesson 第 2 次觸發 → 依制度分層升級（見 CLAUDE.md 分層表與 /lesson skill）。

## 追求優雅（有節制）

- 非平凡修改完成後自問一次：「知道現在知道的一切，還會這樣寫嗎？」感覺 hacky 就重寫。
- 簡單明顯的修法直接過，不過度工程。

## Git 紀律

- 原子 commit：一個 commit 只做一件事；訊息格式 `type(scope): description`（其餘
  git 行為——不 commit 除錯碼、未經要求不 commit/push——內建 harness 指引與
  `commit_guard.py` 已覆蓋，不重述）。

## Changelog

- 2026-08-06：依 eval 實測（t3–t6，Opus 5，A 現行制度 vs C `--safe-mode` 零制度）精簡——
  刪 #14（降為按需，`reporting.md` §1 是完整正本）；#1、#9 前半壓縮（Edit/Write 工具
  與 `backup_gate.py` 已機器強制）；「計畫」節刪第 1 條（內建 plan mode／TaskCreate
  已是機制，保留第 2 條判準要求）；Git 紀律 4→2 行（內建與 `commit_guard.py` 已覆蓋）；
  #11 節首加動機說明，換掉已被平台計價方式反轉的「省額度」理由；不重編號，#15 加
  跳號註記。詳見 `docs/harness-overlap-2026-08.md`（使用者核准）。
- 2026-07-26：rules 按需檔移至 rules-lib/（脫離新版 Claude Code 對 rules/ 的自動常載），路徑引用同步更新（/doctor 健檢，使用者核准）。
- 2026-07-19：#3、#4 加「決策點必填欄位」（已驗證/範圍外發現）——借鑑 fable-method
  的 INTENT/TWINS 機制：散文叮嚀弱模型可能默默跳過，逼一行逐字產物讓漏做一眼可見
  （claude-institution branch feat/mandatory-artifacts，使用者核准）。
- 2026-07-15：新增 #15 寫入後獨立查證——lessons.md「假同步」教訓二次觸發依制度升級；
  不可 hook 化（hook 看不見被注入的假工具輸出）、不可按需化（假輸出何時出現不可預測），
  故進層 1（蒸餾計畫 P1，使用者核准）。
- 2026-07-14：新增 #14 回報結論先行，細節住 reporting.md（Fable 5 session 補蒸餾，使用者核准）。
