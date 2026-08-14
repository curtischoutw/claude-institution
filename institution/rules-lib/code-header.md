# File Docstring 模板（按需）

<!-- 按需引用檔。觸發時機：建立任何新的原始碼檔案之前（CLAUDE.md 路由表指到這裡）。
     2026-07-13 自 code-standards.md 降層——依 diagnosis.md 常載兩題測試，
     模板全文只在建檔時需要，不必每輪常載。
     2026-08-14 改版：砍掉 File/Author/Email/Created Date/Version/Copyright/
     Version History 七個元資料欄位，只留敘述性內容。原因見下方「為什麼砍掉元資料」
     （本 repo 11 個原始碼檔實測：3 個版本欄位已與 git 分歧、11 個 Email 是未填佔位符，
     使用者核准）。 -->

每個產出的原始碼檔案開頭必備模組層級敘述（markdown 設定檔與 SKILL.md 除外），
依語言換用對應的註解符號或 docstring 語法。

**判準一句話：寫下去之後會因為別處改動而變成錯的，就不要寫進檔頭。**

## 模板

```
<這個檔是什麼、為什麼存在、關鍵設計決策>

Features:
  - <對外行為 1>
  - <對外行為 2>

已知極限:
  - <機制上修不掉的限制；沒有就整節省略>

Dependencies:
  - <依賴什麼、為什麼需要>
```

- `Features` 寫**對外可觀察的行為**，不是實作步驟流水帳。
- `已知極限` 寫**機制上修不掉**的限制（不是 TODO）。這是整個檔頭最不可取代的一節——
  git 不會告訴你「這個 hook 擋不下 Bash 直改」。沒有就整節省略。
- `Dependencies` 寫依賴什麼、為什麼需要，**不寫版本號**——版本鎖在套件管理檔
  （`pyproject.toml`／`package.json`／`requirements.txt`），寫進檔頭只會與它分歧。

## 為什麼砍掉元資料

這些欄位不寫，因為 git 已經是它們的事實來源，手抄一份必然分歧，
而分歧時讀者無法判斷哪一份在說謊——**過期的檔頭比沒有檔頭更糟**。

| 不再寫 | 為什麼 | 去哪查 |
|---|---|---|
| `File`（檔名） | 檔案自己知道；改名即失真 | 檔案系統 |
| `Author` / `Email` | 會與實際貢獻者不符 | `git log --format='%an' -- <file>` |
| `Created Date` | 靠人維護只會愈來愈歪 | `git log --diff-filter=A -1 --format=%ad -- <file>` |
| `Version` / `Version History` | 與 git 是兩份紀錄，必然分歧 | `git log -- <file>`、`CHANGELOG.md` |
| `Copyright` | 逐檔重複；授權以根目錄 `LICENSE` 為準 | `LICENSE`（需對外散布的單檔可加一行 `SPDX-License-Identifier: <授權>`） |

變更歷史的正確落點：**Conventional Commits 的 commit message**（寫清楚改了什麼、
為什麼、怎麼驗證的）→ 需要對外的 release 粒度再彙整到 `CHANGELOG.md`。

版本號不放檔名，也不放檔頭。
