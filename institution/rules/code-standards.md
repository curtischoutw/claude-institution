# Code Standards（常載）

## File Docstring

每個產出的原始碼檔案開頭必備模組層級敘述（markdown 設定檔與 SKILL.md 除外）：
這個檔是什麼、為什麼存在、關鍵設計決策、已知極限。

**只寫 git 答不出來的資訊**——作者、Email、建檔日期、版本號、變更歷史一律不寫進檔頭
（手抄一份必與 git 分歧，分歧時讀者無法判斷哪份在說謊；過期的檔頭比沒有檔頭更糟）。
**建立新原始碼檔前，讀 `~/.claude/rules-lib/code-header.md` 取完整模板**——不憑記憶寫。

## In-file Structure

- 功能區塊之間用 `# ==============================` 分隔線 + 標籤。
- 每個 function/method docstring 必含 `Args` 與 `Returns`。
- 版本號不放檔名，也不放檔頭：套件版本在套件管理檔，變更歷史在 git／`CHANGELOG.md`。

## Security Floor（寫碼當下的底線，red-team 審查前就要守住）

- 外部輸入（使用者輸入、API 回應、檔案內容）先驗證再使用（型別、必要欄位存在、長度/範圍），不假設格式正確。
- Secrets（金鑰、token、密碼）永不寫進程式碼、log 或錯誤訊息；一律走環境變數或密鑰管理。
- 組 SQL / shell 指令一律參數化（placeholder / shlex），禁止字串拼接使用者輸入。
- 新增第三方依賴前先回報使用者（名稱＋用途＋為何內建做不到）。

## Core Principles

- **Simplicity First**：每個改動盡可能簡單，影響最少的程式碼。
- **No Laziness**：找根因，不做臨時貼補。
- **Surface Assumptions**：所有假設寫出來，永不沉默猜測。
- **Proactive Warnings**：主動指出風險、邊界情況與副作用，即使沒被問。

## Changelog

- 2026-07-14：新增 Security Floor 節——寫碼當下的安全底線，補 red-team 事後審查的空窗（Fable 5 session 補蒸餾，使用者核准）。
- 2026-07-26：rules 按需檔移至 rules-lib/（脫離新版 Claude Code 對 rules/ 的自動常載），路徑引用同步更新（/doctor 健檢，使用者核准）。
- 2026-08-14：檔頭改為「只留敘述、砍掉元資料」——刪 File/Author/Email/Created Date/Version/Copyright/Version History 七欄，改由 git 與 `CHANGELOG.md` 承擔。理由：本 repo 11 個原始碼檔實測，`rm_guard.py` 的 `Version` 與自身 `Version History` 首行矛盾、`backup_gate.py` 與 `prompt_nudge.sh` 修改後漏更新、11 檔 `Email` 全是未填佔位符；且「什麼算實質修改該不該 bump」不可機器判定，無論放哪層都會腐爛（使用者核准）。
