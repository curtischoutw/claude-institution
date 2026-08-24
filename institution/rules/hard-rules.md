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
4. 修 bug 時發現範圍外的問題：記到 `tasks/todo.md`，不順手修；完工回報必寫一行
   「範圍外發現: <項目，或「無」>」。
5. 宣稱「完成」之前必走 /done-check；回報必附實際指令與輸出，不得只寫「測試通過」。
6. 同一問題修 2 次沒好 → 進 /debug-protocol；第 3 次修改仍失敗 → 停手 revert，
   在協定內重找根因，不准亂槍打鳥。
7. 動手前先估規模：實際規模與使用者描述差一個量級以上（「小修」卻要動 5 個檔）→ 先講再做。
   事後熔斷：自稱「小修」的 diff 超過 3 個檔案、或 `git diff --stat` 增刪合計超過 100 行
   → 停下來先回報，再決定是否繼續。
8. 不確定就寫「我不確定」並說明怎麼驗證；禁止用肯定語氣包裝猜測。
   型號、參數、API 之類的事實：查得到寫實際值，查不到寫「待確認」，絕不憑記憶填。
9. 改 `~/.claude/` 下制度檔前先看 `backup_gate.py`（層 0 hook，會擋無備份的修改）
   與 `~/.claude/rules-lib/maintenance.md` 的權限分級；專案檔靠 git。新內容寫新檔，
   不塞進既有長檔。
10. 隨做隨寫：每完成一個交付項立刻存檔再做下一項。session 隨時可能中斷，存了的才算數。

## 調度硬規則

派工是例外不是常態，與內建 Agent tool 說明同向（「Do not spawn agents unless the user
asks… handle it inline」）。唯一站得住的理由是**中間輸出會淹沒主 context**，不是省額度，
也不是「任務看起來有好幾個面向」。

11. 命中以下任一條才派 subagent，否則主對話直接做完：(a) 中間輸出會淹沒主 context
    （掃 repo、位置不明的大範圍搜尋、批次讀十幾個檔）；(b) 需要 fresh-context 第二意見
    （見 #12）；(c) 使用者明講要派。派法與模型選擇 → `~/.claude/rules-lib/dispatch.md`。
12. 驗證不自驗：修改者不得擔任自己產出的唯一驗證者。重要交付派 fresh-context agent
    做 read-back 或實跑（細節見 dispatch.md「驗證」節）。
13. subagent 回報合約：只回結論與「檔案:行號」，長產物存檔後傳路徑，禁止整檔貼回主對話。
15. 寫入/刪除/覆蓋動作後，同一或緊接指令必用 `test -e`/`diff`/`cmp` 印出磁碟實際狀態
    才可宣稱完成；工具輸出摻任何與指令無關的雜訊 → 一律判為不可信，改用自控格式的獨立指令重驗。
    （編號沿用；原 #14「回報結論先行」已於 2026-08-06 移除並降為按需，見 reporting.md
    §1，故此處由 #13 跳到 #15，不重編以保留 lessons.md 與 CHANGELOG.md 的歷史引用。）

## 計畫

- 計畫每一項必附：**假設**（禁止沉默假設）、**風險**、**完成判準**。
  - 判準壞例：「完成登入功能」。好例：「`pytest tests/test_auth.py` 全綠，且 `curl /login` 回 200 + token」。
- 執行中發現計畫錯了 → 立刻停下重排，不要邊做邊救。方向錯的訊號 → 讀 `~/.claude/rules-lib/judgment.md`。

## 自我改進

- 被使用者糾正（任何形式的「不對」「不是這樣」「我說過」）→ 當下用 /lesson 記入 `tasks/lessons.md`。
- 同一 lesson 第 2 次觸發 → 依制度分層升級（見 CLAUDE.md 分層表與 /lesson skill）。

## Git 紀律

- 原子 commit：一個 commit 只做一件事；訊息格式 `type(scope): description`（其餘
  git 行為——不 commit 除錯碼、未經要求不 commit/push——內建 harness 指引與
  `commit_guard.py` 已覆蓋，不重述）。

<!-- 變更歷史一律在 git 與 repo 的 CHANGELOG.md，不放本檔（2026-08-14 檔頭改版原則，
     2026-08-24 延伸適用到常載規則檔——每 session 載入 27 行歷史不划算）。
     查本檔逐次修改：git log -p -- institution/rules/hard-rules.md -->
