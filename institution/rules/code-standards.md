# Code Standards（常載）

## File Docstring

每個產出的原始碼檔案開頭必備模組層級敘述（markdown 設定檔與 SKILL.md 除外）：
這個檔是什麼、為什麼存在、關鍵設計決策、已知極限。**只寫 git 答不出來的資訊**——
作者、Email、建檔日期、版本號、變更歷史一律不寫進檔頭（過期的檔頭比沒有檔頭更糟）。
**建立新原始碼檔前，讀 `~/.claude/rules-lib/code-craft.md` 取完整模板**——不憑記憶寫。

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

<!-- 原 Core Principles 另兩條 Surface Assumptions／Proactive Warnings 於 2026-08-24 刪除：
     內建 system prompt「Delivering work」節已要求 state your assumption 與
     flagging important factors for the user。
     變更歷史一律在 git 與 repo 的 CHANGELOG.md，不放本檔。
     查本檔逐次修改：git log -p -- institution/rules/code-standards.md -->
