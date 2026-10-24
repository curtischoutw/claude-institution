# Code Standards

## File Docstring

每個原始碼檔案開頭寫模組層級敘述（markdown 設定檔除外）：這個檔是什麼、為什麼存在、
關鍵設計決策、已知極限（機制上修不掉的限制，沒有就省略）、Dependencies（不寫版本號）。
只寫 git 答不出來的資訊：作者、Email、建檔日期、版本號、變更歷史一律不寫進檔頭。

## Security Floor

- 外部輸入（使用者輸入、API 回應、檔案內容）先驗證再使用（型別、必要欄位、長度／範圍）。
- Secrets（金鑰、token、密碼）永不寫進程式碼、log 或錯誤訊息；走環境變數或密鑰管理。
- 組 SQL／shell 指令一律參數化（placeholder／shlex），禁止字串拼接使用者輸入。
- 新增第三方依賴前先回報使用者（名稱＋用途＋為何內建做不到）。
