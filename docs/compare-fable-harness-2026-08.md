# claude-institution vs fable-harness 比較：2026-08-24

<!-- 目的：供使用者判斷「要不要整合、整合哪些」。本檔只做比較與分類，**不做整合決策**，
     也不代替使用者選邊。判定所依據的 harness 內建行為，出處為 Claude Code 2.1.241
     官方文件（memory / features-overview / commands / hooks）與本次 session 可直接
     讀到的內建 system prompt，逐項查證，不憑記憶。
     比較對象版本：fable-harness v1.0.2（commit 9b949b3，upstream Miguok/fable-harness）。
     日後重跑方式見文末「下次覆核怎麼用這份文件」。 -->

## 0. 一句話結論

兩者不是競品，是**同一套 hook 機制的兩個分支**：`claude-institution` 的 `verify_gate.py`、
`prompt_nudge.sh` 與三個對抗 agent 明文取材自 `fable-harness`，之後各自往不同方向長。
`fable-harness` 往「**可散佈、可安裝、有 e2e 測試的行為協議產品**」長；
`claude-institution` 往「**可演化、可證偽、與 harness 持續對齊的個人制度**」長。
因此值得吸收的多半是 fable 的**工程化**部分，而非它的規則內容——它的規則內容與
`claude-institution` 高度重疊，且有幾條已被 2.1.241 內建覆蓋或反轉。

---

## 1. 定位與血緣

| | claude-institution | fable-harness |
|---|---|---|
| 本質 | 個人 `~/.claude/` 的版控快照＋制度演化實驗場 | 公開可安裝的 drop-in 行為協議 kit |
| 上游 | `curtischoutw/claude-institution` | `Miguok/fable-harness` v1.0.2（MIT） |
| 讀者 | 只有作者自己 | 任何人 |
| 安裝 | `restore.sh`（覆寫前自動備份） | `INSTALL.md` 9 步，由使用者的 Claude Code 自己執行；**canary 驗證**（新 session 問「協議代號」須答 `FABLE-PROTOCOL-V1-CANARY`） |
| 版本策略 | `CHANGELOG.md`，無版號 | SemVer + `VERSION` 檔，MAJOR/MINOR/PATCH 定義綁在**協議契約**上（hook/skill/agent 被移除或改名＝MAJOR） |
| 在地化 | 全繁中 | 五語 README（en/zh-TW/zh-CN/ja/ko）＋ zh-TW LICENSE |
| 規模 | 53 檔 / 4343 行（.md 2565） | 27 檔 / 1620 行（.md 706） |

**血緣證據**（`claude-institution` 自己寫的，非本次推論）：

- `README.md:121`「借鑑自 Miguok/fable-harness 的同款機制，判斷邏輯保留、訊息改寫成
  指向本專案自己的規則；不引入 fable 的 FABLE-PROTOCOL 命名或協定文字。」
- 三個 agent 正文各有一行「取材自 Miguok/fable-harness 的 <name> subagent 設計，
  綁回本專案自己的判準」。
- `hard-rules.md` Changelog 2026-07-19：「借鑑 fable-method 的 INTENT/TWINS 機制」。
- `tasks/todo.md` 末條 Deferred：「規則准入紀律（借鑑 fable-method prime directive）」。

所以「整合」在這裡的實際意義是**回頭把上游後來長出的東西擇優搬回來**，而不是合併兩個
陌生系統。

---

## 2. 同一機制的兩種實作（逐項對照）

| 機制 | claude-institution | fable-harness | 差在哪 |
|---|---|---|---|
| **協議進 context 的方式** | `~/.claude/CLAUDE.md`＋`rules/` 無 `paths:` frontmatter 自動常載，183 行 | `SessionStart` hook `inject_protocol.sh` 把 `fable_protocol.md` 40 行 `cat` 進 context | fable 的方式**不受 200 行 CLAUDE.md 建議上限管轄**，但也不被 `/context` 的 Memory files 列出、`/doctor` 看不到；institution 的方式是官方文件明載的機制 |
| **verify_gate** | 294 行 / 45 副檔名；除測試指令外，**語法檢查指令**（`py_compile`、`bash -n`…）與**派出含驗證意圖的 Task/Agent** 也算證據 | 147 行 / 24 副檔名；只認測試指令 | institution 的判定面更寬（少誤擋），fable 的更嚴（少漏放）。兩者都 fail-open、都用 `stop_hook_active` 二次 Stop 放行防卡死 |
| **fail-open 之後呢** | 寫 `~/.claude/hooks/hooks.log` | 追加一行到 gitignored `.gate_fail`，上限 500 行、**保留最早**的事件、只記例外類別＋截斷訊息、絕不記 raw payload；telemetry 本身包在巢狀 try 內 | fable 的設計更克制且明確；institution 的 hooks.log 已達 64 KB，無上限、無輪替 |
| **對抗審查** | `uplift.md` 方法 2/3 ＋ 三個 agent，**無機械裁決規則** | `adversarial-review` skill：三 agent 單則訊息平行派出、**過半存活制**（3 存活＝直接採信／2＝採信但必須把 REFUTED 理由列進風險／≤1＝結論擋回）、loop-until-dry（影響生產者連 2 輪無新發現才收工）、併發預算每輪 ≤2 findings | fable 有可判定的收斂條件，institution 只有流程 |
| **派工規格** | `dispatch.md` 三要素（目標與動機／驗收條件／回報格式），缺一不發 | `model_dispatch_rules.md` **7 欄派工包**：目標／範圍／**非目標**／**允許路徑**／驗收標準／回報格式／**停止條件**；缺任一欄＝無效派工，子代理須先要求補齊 | fable 多出的三欄（非目標、允許路徑、停止條件）institution 完全沒有 |
| **回報合約** | hard-rules #13：只回結論與「檔案:行號」，長產物存檔傳路徑 | 5 欄模板：結果 TLDR／做了什麼／**證據**／**超出範圍發現**／**風險與未完成**（後兩欄「真的沒有」也要寫理由，不得空白） | 兩邊精神一致，fable 的是可檢查的模板 |
| **停損計數** | hard-rules #6：同一問題修 2 次→`/debug-protocol`；第 3 次→停手 revert | **三個計數器明確分離並互相交叉註記防混淆**：自我重試 2 次連續失敗→換路；子代理交回實質錯誤 1 次→升級；發現自己在「猜」而非「推導」→第 2 次猜之前就升級 | institution 只有一個計數器；fable 在 `cognitive_rubrics.md` 與 `model_dispatch_rules.md` 雙向註記「這三個數字管的是不同主體，別合併」 |
| **備份** | `backup_gate.py` 機器強制，但**只管 `~/.claude/` 制度檔**；專案檔靠 git | CLAUDE.md 守則 3：改**任何**既有檔前建 `<檔名>.bak.<YYYYMMDD-HHMMSS>` 並確認存在，**備份失敗＝停** | institution 是機器強制但範圍窄；fable 是 prompt 層但範圍全覆蓋。fable 的做法在 git repo 內會製造大量 `.bak.*`（其 `.gitignore` 確實有這條） |
| **自我改進迴圈** | `tasks/lessons.md` → 第 2 次觸發依分層升級到 hook／常載／skill；有一個完整閉環實例（hard-rules #15） | **無** | institution 獨有 |
| **測試** | `eval/` 6 題人工評分，測「制度是否提升**產出品質**」；hooks 本身**零測試** | `tests/test_verify_gate.py` 12 案例 363 行 e2e，測「hook **行為**是否正確」；無產出品質評測 | 兩邊測的是完全不同的東西，**互補而非重複** |
| **模型路由** | 2026-08-06 已刪除靜態型號表，理由：「會過期的事實表」，改成兩行原則 | 靜態表：推理→當前模型（不指定 model）／編碼→`sonnet`／批次搜尋→`haiku`；三反方 floor 強制 `model: opus` | **直接衝突**，見 §5 |
| **三個對抗 agent 的 frontmatter** | `name` / `description` / `tools`，**無 `model:`** | 同樣**無 `model:`** | 實測兩邊皆無——fable 的 `model: opus` floor 純粹是 protocol §5 與 SKILL.md 的 prompt 層要求，**無機器強制**（`.claude/agents/*.md` 可用 `model:` frontmatter 做到，兩邊都沒用） |

---

## 3. fable-harness 獨有、值得判斷是否吸收（12 項）

依「吸收價值 ÷ 吸收成本」排序。前三項是我認為最值得的。

### 3.1 hooks 的 e2e 測試套件 ★最大缺口

`tests/test_verify_gate.py` 12 案例 363 行，且每個案例都可追溯到一次真實失效：

- T9 多生態測試指令（mvn/gradle/dotnet/rspec/phpunit/ctest/make test/tox）→ 來自「紅隊
  R1」發現的 Java/C#/Ruby/PHP 專案被系統性誤擋。
- T10 假放行防護（`cat tox.ini`、`make testdata`、`npm run testbed`、`mvn test-compile`
  這類「長得像測試指令」的日常指令仍須擋）→ 來自「紅隊 R4」。
- T11 `--test` 自測入口放行，但 `--test-pypi`／`--testing`／`--tests` 仍擋 → 來自一次
  真實 session 中 `zh_convert_safe.py --test` 連續被誤擋四次。
- T12 內部例外（payload 缺 `transcript_path`）仍 fail-open（rc 0、stdout 空），
  但 `.gate_fail` 必須剛好多一行且**不含 raw payload**。

**實測確認**：`claude-institution` 的 5 個 hooks（1072 行，含 443 行的 `rm_guard.py`）
**沒有任何測試**——repo 內唯一的 `test_*.py` 是 `eval/fixtures/test_refactor_target.py`，
那是評測題目的 fixture，不測 hook。`rm_guard.py` 是全 repo 風險最高的檔（判斷錯誤＝
誤擋正常刪除，或漏擋災難刪除），卻只有 docstring 裡的 5 條已知極限，沒有一個可重跑的
案例。

> 這一項與 §4 的「eval 產出品質評測」互補，不衝突：eval 測制度有沒有用，e2e 測 hook 有沒有壞。

### 3.2 7 欄派工包的後三欄

`claude-institution` 的三要素沒有：

- **非目標 Non-goals**（至少 1 條，明擺著防「順手改」）
- **允許路徑 Allowed paths**（可讀清單＋可寫清單，**寫入預設禁止除非明列**）
- **停止條件 Stop conditions**（遇到什麼立刻停：範圍外檔案、編譯錯誤、機密、需要刪東西）

輕量唯讀派工可以把其中三欄填「預設」，**但欄位本身不得省略**——這正是 institution
`hard-rules.md` #3/#4「逼一行逐字產物讓漏做一眼可見」的同一手法，只是用在派工上。

### 3.3 過半存活裁決制

`uplift.md` 方法 2（多答案評審擇優）與方法 3（對抗自查）目前只寫「怎麼做」，沒寫
「做完怎麼算」。fable 的三檔判準是機械的：3 存活→採信；2 存活→採信但 REFUTED 理由
必須進風險列表；≤1 存活→**結論擋回**，改完重送。外加 loop-until-dry 的收斂條件與
「每輪最多 2 個 findings（併發預算 6 個 subagent）」「N 個獨立發現必須逐個抗辯，
禁止打包」的資源規約。

### 3.4 收工自檢

> 結束前檢查自己的最後一段——若它是「接下來我會…」的承諾或計畫而非已完成的結果，
> 就算未完成；做完再結束。

一行，可自檢，institution 的 `reporting.md` 沒有等價條文。

### 3.5 「註解與參數說明是受保護內容」

> 即使在優化邏輯，也不得刪除參數說明、既有註解、交易假設、歷史註記。
> **未經指示的刪除是失敗，不是清理。**

institution 的 `code-standards.md` 只規範「要寫什麼檔頭」，沒有「不准刪別人的註解」。
考量到內建 `/simplify` 會主動做 cleanup，這條的防護價值反而上升。

### 3.6 出界即停的還原程序

子代理動到 Scope 外的檔 → 立刻停 → 先把該檔複製成 `.bak`（**壞掉的狀態也是證據**）→
`git diff` 定位 → **只還原出界的部分** → 回報「動了 X，已還原」。
並附警告：**整檔 `git checkout` 會連範圍內未提交的修改一起不可逆丟掉，禁止當作預設動作**。

institution 的 hard-rules #7 只有「diff 超標就停下回報」，沒有還原程序。

### 3.7 `.gate_fail` 式的 fail-open 遙測

見 §2 表。institution 的 `hooks.log` 已 64 KB 且無上限、無輪替、不區分「正常紀錄」與
「fail-open 事故」。

### 3.8 `.gitattributes` 強制 LF

`*.sh text eol=lf`，理由寫在檔內：**CRLF shebang（`#!/bin/bash\r`）會讓 hook 直接死掉**。
institution 沒有 `.gitattributes`；目前只在 macOS 用不會踩到，但 `restore.sh` 與 5 個
hook 都是 shell/python 腳本，一旦在 Windows 或跨平台 checkout 就會中。

### 3.9 §6 Harness 分流 ＋ `detect_harness.py`

專案若已啟用專用開發 harness（harnessmith / Superpowers），該 harness 擁有 SDLC 主流程，
fable 只保留 §1–4 底線，**不搶主流程、不疊第二套派工系統**。配套 235 行唯讀偵測器
輸出 JSON 建議（`use-detected-harness-as-main-flow` / `ask-user` / `no-special-routing`），
**從不自動接管、從不自動關閉自己**。

institution 沒有等價概念——它預設自己是唯一制度。若日後在別人的 repo 工作，這是
唯一處理「兩套制度疊加」的現成設計。

### 3.10 「綠燈必要但不充分」

> 測試綠是必要條件不是充分條件：關鍵行為必須走真實流程、從外部觀察到
>（hook 真的觸發了、頁面真的變了）才算驗證。

institution 的 `/done-check` 步驟 3「手動走 happy path」精神相近，但沒有把這句寫成
Definition of Done 的一部分。

### 3.11 三個計數器分離

見 §2 表。institution 目前只有 hard-rules #6 一個計數器，`dispatch.md` 的升降級路徑
（haiku 錯 1 次→sonnet；sonnet 連錯 2 次→opus）其實是第二個計數器，兩者關係只在
`dispatch.md` 註記了一句，不像 fable 那樣雙向交叉註記。

### 3.12 特殊語法檔鐵則

PowerLanguage / EasyLanguage / Pine Script / SQL migration / CI YAML 編譯或語法錯誤 →
收集**完整逐字錯誤訊息** → 升級；**嚴禁盲目重試**（每次盲試都燒 token 且常常越弄越糟）。

領域性強（作者顯然做交易策略），但「編譯錯誤不盲試、先收集完整錯誤再升級」這條可以
一般化，institution 的 `/debug-protocol`「禁止事項」沒有這條。

---

## 4. claude-institution 獨有（10 項）

反向清單，供判斷「整合時不能弄丟什麼」。

1. **五層制度分層（層 0–4）＋常載准入兩題**：加常載規則前必答「能不能做成 hook？
   能不能放按需檔？」，兩題都「不能」才准進常載。fable 沒有分層概念，所有規則平鋪。
2. **lessons 升級迴圈**：被糾正→記 `tasks/lessons.md`→第 2 次觸發→依分層升級。
   有一個完整閉環實例（hard-rules #15 由「假同步」教訓二次觸發升級而來）。
3. **eval 可證偽性承諾**：「得分比與估計差 >10 個百分點就回來改本檔」「重大改版後
   重跑 eval，把增益歸因到具體制度件，**砍掉沒有增益的規則**」。fable 沒有任何
   衡量自身是否有效的機制——它的 363 行測試測的是 hook 行為，不是協議價值。
4. **harness 重疊覆核法**：`docs/harness-overlap-2026-08.md` 與「**理由比規則更早
   過期——覆核先問理由，不是只問要不要**」這條教訓。fable 的 governance 文件裡沒有
   任何「與 harness 內建重疊」的概念，它的 §5 靜態模型表就是這個缺口的直接後果。
5. **`rm_guard.py`（443 行）＋`backup_gate.py`＋`commit_guard.py`**：fable 只有
   `verify_gate.py` 一個 gate。`rm_guard` 處理 `~`/`$HOME` 展開、casefold 比對、
   剝除 `sudo`/`env` 包裝、`bash -c`/`eval` 內聯遞迴、逐段追蹤 `cd`/`pushd`——
   fable 完全沒有災難刪除防護。
6. **`settings.json` 的 `permissions.deny` 11 條**：由 Claude Code 自身解析，
   不依賴 Python，是缺直譯器時的最後防線。fable **根本沒有 `settings.json`**（見 §6）。
7. **誠實條款凌駕全部的條文優先序**：誠實條款 > hard-rules > 按需檔/skills >
   lessons.md。fable 的守則 5 只說「規則衝突時選較安全、較窄、可逆的動作」，沒有排序。
8. **三個逐字必填欄位**：「已驗證: <結論>」「範圍外發現: <項目或無>」
   「AUTH: 使用者說「<原話>」」（找不到原話＝未授權）。fable 的回報模板有類似效果，
   但沒有 AUTH 這種「引用使用者原話」的授權留痕。
9. **ADHD 友善回報條款**（`reporting.md` §5）：可見進度、一個 <2 分鐘的下一步、
   具體估計。經 `docs/i-have-adhd-skill-assessment.md` 評估後蒸餾而來。
10. **對抗 agent 的反編造條款**：institution 版明訂「不得為了判 REFUTED 而編造牽強
    反例」「判『不適用』須寫依據」；fable 版只說「不確定時傾向 REFUTED」。
    這是 institution 版**優於**上游的一處。

---

## 5. 六個直接衝突（整合時必須擇一）

| # | 衝突 | claude-institution | fable-harness | 備註 |
|---|---|---|---|---|
| 1 | **靜態模型路由表** | 2026-08-06 已**刪除**，判定為「會過期的事實表」，與 hard-rules #8「不憑記憶填型號」同理 | CLAUDE.md ＋ protocol §5 雙處硬寫「編碼→sonnet／批次→haiku」 | institution 這邊有明確論證與先例（2026-07-13 已因同理由刪過型號參數表）。吸收 fable 的表＝推翻自己一年前的判定 |
| 2 | **三反方 model floor** | `dispatch.md` 要求「必顯式指定 model，不留空繼承」 | 要求「一律 `model: opus`，除非主迴圈 ID 含 `opus` 或 `fable` 才可繼承」 | 方向相反：一個要求明指，一個在特定條件下要求繼承。**兩邊都無機器強制**（agent frontmatter 都沒有 `model:`） |
| 3 | **「指揮官不下場」的觸發強度** | hard-rules #11「一律派」（本次精簡已決定改為條件式） | 機械觸發：預估讀 >10 檔／grep >100 行／「找出所有 X」句型 | **兩邊都與 2.1.241 內建對撞**——內建 Agent tool 現行原文：「Do not spawn agents unless the user asks… handle it inline with your own tools.」fable 的版本比 institution 更難調和 |
| 4 | **備份範圍** | 只管 `~/.claude/` 制度檔，機器強制 | 管**任何**既有檔，prompt 層，備份失敗＝停 | fable 版在 git repo 內會製造大量 `.bak.*`；但 institution 的窄範圍在非 git 目錄下是真空 |
| 5 | **協議注入方式** | `rules/` 自動常載 | `SessionStart` hook 注入 | **兩者疊加會重複載入同類規則**——這是「矛盾指令→模型任意選邊」的教科書情境（官方 memory 文件明文警告）。整合時必須二選一 |
| 6 | **雙源同步 vs 單一正本** | `maintenance.md`：新內容寫新檔，不重述，避免漂移 | CLAUDE.md 明文規定「改模型分工表**必須同步改** protocol §5」，並在三處重複同一段 floor 條文 | fable 自己也承認這是最脆弱的耦合。institution 的原則更好，但代價是規則散在更多檔 |

---

## 6. fable-harness 的已知缺陷（整合前必知，全部實測確認）

| # | 缺陷 | 證據 |
|---|---|---|
| 1 | **`.claude/settings.json` 不存在**，但 `MAINTAINING.md:13` 與 zh-TW 版都宣稱「`.claude/settings.json` sets `attribution`」 | `ls -la fable-harness/.claude/` 只有 `agents/`、`hooks/`、`skills/` 三個目錄 |
| 2 | **`ROADMAP.md` 不存在**，但 `scripts/detect_harness.py` **引用 8 次**，其中 module docstring 第一行就寫「ROADMAP.md §4.1 為權威 spec」 | `grep -c ROADMAP scripts/detect_harness.py` → 8 |
| 3 | `CLAUDE.md:42` 說「佈署步驟見 README.md」，但 README 的 Quick start 只說「照 INSTALL.md 做」，**自己沒有部署步驟** | `grep -n -i 'deploy\|install' README.md` |
| 4 | `CLAUDE.md:42` 硬編碼 Windows 路徑 `C:\Users\user\.claude\`，而 `INSTALL.md` 正確處理雙平台 | 同上行 |
| 5 | `verify_gate.py:12` docstring 說「十二案例」，`cognitive_rubrics.md:15` 仍說「十個案例」（T11/T12 加入後未同步） | 兩處 grep 命中 |
| 6 | 三個 agent **無 `model:` frontmatter**，`model: opus` floor 是純 prompt 層要求，無機器強制 | `grep -l 'model:' .claude/agents/*.md` 無命中 |

第 1、2 項意味著**這個 repo 的 governance 文件與實際內容已經脫節**；吸收它的規則時
不能假設文件描述等於實作。第 6 項與 institution 現況相同，不是差異。

---

## 7. 兩者對現行 2.1.241 內建的重疊（同一把尺量兩邊）

`claude-institution` 已用 `docs/harness-overlap-2026-08.md` 做過一輪，本次精簡再做一輪。
`fable-harness` **從未做過**，用同一把尺量，它有以下條文已被內建覆蓋：

| fable 條文 | 內建等價 | 判定 |
|---|---|---|
| protocol §1 Observe「嚴禁未讀先猜」 | Edit tool：「You must Read the file in this conversation before editing, or the call will fail」 | 已機器強制 |
| protocol §1 Orient「假設明講、多重讀法列給使用者選」 | system prompt `Delivering work`：「state your assumption or ask your question to the user at the right time」 | 重疊 |
| protocol §3 回報紀律「第一句就是結果」「誠實回報失敗」 | system prompt：「Report outcomes faithfully: if tests fail, say so with the output」 | 重疊 |
| protocol §5 靜態模型表 | 無內建等價，且違反「不憑記憶填型號」——型號會過期 | **已過期** |
| protocol §2 多方抗辯 | bundled skills `/code-review`（含 `ultra` 多 agent 雲端審查）、`/simplify`、`/security-review` | 部分重疊；fable 的過半存活裁決仍是內建沒有的 |
| CLAUDE.md 守則 5「衝突時選較安全、較窄、可逆」 | system prompt：「For actions that are hard to reverse or outward-facing, confirm first」 | 重疊 |
| `cognitive_rubrics.md`「何時問人」的不問清單 | system prompt `Delivering work`：「Reserve blocking questions… for cases where proceeding under any assumption would be unsafe」 | 重疊 |

**結論**：fable 的「規則內容」約有一半已被 2.1.241 內建吸收，且它沒有覆核機制會持續
偏離。**值得吸收的是它的工程化資產（§3.1–3.3、3.7、3.8），不是它的協議文字。**

---

## 8. 下次覆核怎麼用這份文件

1. 先確認上游版本是否前進：`git -C fable-harness log --oneline -5` 與 `cat VERSION`。
   本檔比較的是 **v1.0.2 / commit 9b949b3**。
2. §6 的六項缺陷逐項重跑（都是一行 `ls` 或 `grep`）——若上游已修，該項從缺陷降為
   「已解決」，且第 1、2 項若修好會提高其 governance 文件的可信度。
3. §7 的內建等價欄位比照 `docs/harness-overlap-2026-08.md` 的規約重查：
   **用 WebFetch／WebSearch 查官方文件，不要憑記憶**。
4. §3 的 12 項若有任何一項被吸收，把它從本表移到 §4（institution 獨有），
   並在 `CHANGELOG.md` 記錄吸收來源與版本。
5. 本檔不做整合決策。整合與否、整合哪幾項，由使用者判斷後另開任務。
