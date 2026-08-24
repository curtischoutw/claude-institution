# 寫碼前：設計 heuristics ＋ File Docstring 模板（按需）

<!-- 按需引用檔。觸發時機：設計新模組／公開 API／資料結構，或建立任何新的原始碼檔案
     （CLAUDE.md 路由表指到這裡）。
     2026-08-24 由 design-heuristics.md（2026-07-14 建）與 code-header.md（2026-07-13
     自 code-standards.md 降層，2026-08-14 砍元資料改版）合併——兩者觸發時機相同，
     且合併後刪去在 Opus 5 上屬常識的正反例。變更歷史見 git 與 CHANGELOG.md。
     與 simplifier／`/simplify` 的分工：本檔是「動手前」把設計帶對方向，它們是
     「交付前」抓過度工程——前者防患，後者補漏，不重複。 -->

## A. 設計 heuristics（動手前過一遍當 checklist，各 ≤30 秒）

1. **Rule of three**：同一模式第 2 次出現 → 複製並加註 `# duplicated from <位置>`；
   第 3 次才抽共用（此時有 3 個真實案例，看得出哪裡真的共通）。還沒第 2 次就想
   「以後可能用到」→ 不抽象。
   - 反例：寫第一個 API client 就先做 `BaseClient` 抽象類——只有 1 個案例的抽象必然
     抽錯維度，之後每個新 client 都在跟它打架。

2. **先寫呼叫端再寫實作**：要新增公開函式／類別／endpoint → 先寫 3–5 行「理想中呼叫端
   長什麼樣」（測試或註解裡的虛構碼皆可），對這個形狀滿意了才寫實作。形狀由使用場景
   決定，不由實作方便決定。

3. **資料結構先於邏輯**：出現平行陣列、對同一欄位判空 ≥3 處、或同一個 key 的
   `dict.get(k, default)` 散布 ≥3 處 → 停下來重看資料模型（該用 dataclass、該正規化、
   該把可選欄位拆成兩型別）。資料模型對了，邏輯自然變短。
   - 正例：`names[]`／`ages[]`／`emails[]` 三個平行陣列靠 index 對齊 → 改成
     `list[Person]`，三處 zip 邏輯直接消失。

4. **模組邊界跟著「一起變更」切，不跟名詞分類切**：拆檔前問「哪些程式碼總是在同一個
   需求裡一起被改？」一起變的放一起。若每個小需求都要同時動 3 個「分類整齊」的檔
   （models.py／views.py／utils.py 各改一行）→ 邊界切錯了，改按功能聚合。

5. **錯誤處理三選一**（選不出來就是還沒想清楚）：(a) 就地處理——這一層有足夠資訊修復
   或重試；(b) 向上拋——原樣拋或包一層加 context，讓知道的人決定；(c) 記錄後降級——
   功能非關鍵、失敗可接受，log warning ＋ 回退行為，且**回退行為要寫進 docstring**。
   `except: pass` 與「catch 後只 return None 不記錄」不屬於任何一類，一律禁止
   （與 /debug-protocol 禁止事項一致）。
   - 反例：資料庫寫入失敗被 `except Exception: return None` 吞掉，呼叫端以為成功
     → 資料默默丟失，最貴的一種 bug。

與設計有關的高風險取捨（兩個方案差很多、影響 ≥1 天）→ 升級用 `uplift.md` 方法 1/2。

## B. File Docstring 模板

每個產出的原始碼檔案開頭必備模組層級敘述（markdown 設定檔與 SKILL.md 除外），
依語言換用對應的註解符號或 docstring 語法。

**判準一句話：寫下去之後會因為別處改動而變成錯的，就不要寫進檔頭。**

```
<這個檔是什麼、為什麼存在、關鍵設計決策>

Features:
  - <對外可觀察的行為，不是實作步驟流水帳>

已知極限:
  - <機制上修不掉的限制（不是 TODO）；沒有就整節省略>

Dependencies:
  - <依賴什麼、為什麼需要；不寫版本號>
```

- `已知極限` 是整個檔頭**最不可取代**的一節——git 不會告訴你「這個 hook 擋不下 Bash 直改」。
- `Dependencies` 不寫版本號：版本鎖在套件管理檔（`pyproject.toml`／`package.json`／
  `requirements.txt`），寫進檔頭只會與它分歧。

**不寫元資料**（`File`／`Author`／`Email`／`Created Date`／`Version`／`Version History`／
`Copyright`）：git 已是它們的事實來源，手抄一份必然分歧，分歧時讀者無法判斷哪份在說謊——
**過期的檔頭比沒有檔頭更糟**。查法：`git log -- <file>`、
`git log --diff-filter=A -1 --format=%ad -- <file>`、根目錄 `LICENSE`
（需對外散布的單檔可加一行 `SPDX-License-Identifier: <授權>`）。

變更歷史的正確落點：**Conventional Commits 的 commit message**（改了什麼、為什麼、
怎麼驗證的）→ 需要對外的 release 粒度再彙整到 `CHANGELOG.md`。版本號不放檔名也不放檔頭。
