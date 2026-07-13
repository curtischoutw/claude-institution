# Todo（範圍外發現，待使用者決定）

## ~~README.md「檔案清單」與 institution/hooks/ 實際內容不符~~（2026-07-12 已解決）

已於本次任務一併修正：`rm_guard.py` 補進 `institution/hooks/`，README 的 hooks
（2→5 檔）、rules（9→10 檔，補 `final-assessment-fable5.md`）、memory（2→3 檔）
小節與「共 24 檔」總數（→29）皆已校正並與 `find institution -type f | wc -l`
的實算結果一致。

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
