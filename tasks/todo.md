# Todo（範圍外發現，待使用者決定）

## ~~README.md「檔案清單」與 institution/hooks/ 實際內容不符~~（2026-07-12 已解決）

已於本次任務一併修正：`rm_guard.py` 補進 `institution/hooks/`，README 的 hooks
（2→5 檔）、rules（9→10 檔，補 `final-assessment-fable5.md`）、memory（2→3 檔）
小節與「共 24 檔」總數（→29）皆已校正並與 `find institution -type f | wc -l`
的實算結果一致。

## README.md「institution/backups/（今日 4 個 .bak）」措辭過期（2026-07-12 fresh-context 驗證發現）

- **現況**：README「### institution/backups/」小節寫「今日 4 個 .bak」，但這 4 個檔案的
  實際 mtime 是 2026-07-05／2026-07-06，非撰寫本次任務當下（2026-07-12）。
- **發現脈絡**：本次任務（rm_guard.py 收錄與檔案清單校正）的 fresh-context 驗證 agent
  順帶核對時發現，與本次任務範圍無關，依 hard-rules #4 不順手修。
- **建議**：把「今日」改成具體日期（如「2026-07-05／06 建立的 4 個」）或改成不含時間
  相對詞的敘述，避免隨時間推移持續誤導讀者。
