# Changelog

本檔記錄 repo 層級的顯著變更。格式參考 [Keep a Changelog](https://keepachangelog.com/)。

日常變更以 Conventional Commits 記在 commit message（改了什麼、為什麼、怎麼驗證的）；
本檔只收「之後回頭看還會想知道」的層級。逐檔的修改紀錄請用 `git log -- <file>`。

## [Unreleased]

### Added

- **快照補上 `settings.json` 與 `statusline.sh`，堵住災難還原缺口**（2026-08-18）。
  三邊對齊調查（repo／`~/.claude/`／遠端 GitHub）發現：`institution/` 快照有 5 個
  hooks 檔本身，卻沒有「把 hook 掛上去」的 `settings.json`（`permissions.deny` ＋
  PreToolUse/Stop/UserPromptSubmit 綁定）——災難還原後 hooks 會全部躺著不生效。
  新增 `institution/settings.json`（hook 路徑去識別化為 `<username>`）與
  `institution/statusline.sh`（無個人化資訊），`restore.sh` 新增 `--with-settings`
  （還原時用 `whoami` 自動替換路徑，不需手動回填）；`statusline.sh` 隨預設流程
  還原。過程中順手修掉 `restore.sh` 一個既有 bug：macOS 內建 bash 3.2 在
  `set -u` 底下對 `$變數` 緊接全形標點（無空格分隔）會誤判為 unbound variable，
  改用 `${變數}` 大括號寫法繞過。

### Changed

- **檔頭規則改版：砍元資料，留敘述**（2026-08-14）。
  `code-header.md` 模板刪去 `File`／`Author`／`Email`／`Created Date`／`Version`／
  `Copyright`／`Version History` 七個欄位，只保留敘述、`Features`、`已知極限`、
  `Dependencies`；`code-standards.md`、`CLAUDE.md` 路由表、`README.md`、
  eval 評分項（`t1-implement-cli.md`、`results/TEMPLATE.md`）同步更新，
  11 個既有原始碼檔的檔頭一併改寫。

  理由：這些欄位與 git 是兩份紀錄，必然分歧，分歧時讀者無法判斷哪份在說謊。
  本 repo 實測——`rm_guard.py` 的 `Version: 1.0.0` 與自身 `Version History` 首行
  `1.2.1` 互相矛盾；`backup_gate.py` 在 `8e37461` 改了 user-facing 訊息卻沒補紀錄；
  `prompt_nudge.sh` 建檔後兩次修改仍是 `1.0.0`；11 個檔的 `Email` 全是未填佔位符。
  且「什麼算實質修改、該不該 bump」不可機器判定，依本制度的分層原則
  （機器可判定才放得進層 0），這條規則無論放哪層都會腐爛。

  對應地新增本 `CHANGELOG.md`，承接原本散在各檔 `Version History` 的內容。

---

## 歷史（自各檔 Version History 一次性彙整，2026-08-14）

以下由原本 11 個原始碼檔的 `Version History` 欄位彙整而來，依時間排序。
彙整後原欄位已從各檔移除；更完整的紀錄見 `git log`。

### 2026-08-07

- `verify_gate.py`：補語法檢查類指令為驗證證據（新增 `SYNTAX_CHECK_RE`）。編輯
  `hooks/*.py` 這類沒有測試套件覆蓋的檔案時，慣用的 `python3 -c ast.parse`／
  `py_compile`／`sh -n`／`bash -n`／`node -c` 原本會被誤判為「沒有測試證據」。

### 2026-07-26

- `restore.sh`：新增 `rules-lib/` 還原迴圈——rules 按需檔搬離 `rules/` 至
  `rules-lib/`（脫離新版 Claude Code 對 `rules/` 的自動常載）後需同步涵蓋。

### 2026-07-15

- `restore.sh`：hooks 預設不還原，需 `--with-hooks` 才覆蓋——快照 hooks 是去識別化
  版本，整包還原會劣化 `~/.claude/` 正本。
- 新增 eval fixtures：`buggy_stats.py`（t3 除錯）、`flaky_cache.py` 與
  `repro_flaky_cache.py`（t4 間歇性除錯）、`refactor_target.py` 與
  `test_refactor_target.py`（t2 重構）。

### 2026-07-11

- `rm_guard.py`：初版建立（使用者要求防止誤刪家目錄／根目錄），並經三輪對抗審查修補：
  - 第一輪：`bash -c`／`eval` 內聯 shell 遞迴檢查、`find -exec` 子指令檢查、
    路徑 casefold、glob 補 dotfile 清空手法；記載 `rm -rf "~"` 誤擋為已知極限。
  - 第二輪：glob 判定由枚舉改規則式（含 `.??*` 與 `{.,}*` brace expansion）、
    逐段追蹤 `cd`/`pushd`、`find` 前置選項（`-L` 等）不再讓起始路徑逃檢；
    片段切割改用 shlex punctuation 模式（引號感知；子 shell 括號也納入檢查）。
  - 第三輪：剝除 shell 群組／流程控制前導 token（`{ } ! do then else`），
    `{ rm -rf ~ ; }` 與 for/if 包裹的刪除不再逃檢。

### 2026-07-06

- `backup_gate.py` 初版（紅隊審查 M3）：機器強制 hard-rules #9 的備份要求。
- `commit_guard.py` 初版（紅隊審查 M4）：機器強制「不 commit 除錯碼」。
- `verify_gate.py`：紅隊審查修補——認可 subagent 驗證（修層 0／層 1 激勵相反）、
  測試指令比對綁指令位置（堵 `cat pytest.ini` 夾帶）、補
  `.ipynb`/`.tf`/`.pl`/`.pm`/`.groovy` 副檔名、fail-open 與 block 寫 log 留痕、
  明文記載已知極限。

### 2026-07-05

- `verify_gate.py` 初版：本制度第一條機器強制規則（層 0），改寫自
  fable-harness 的 `verify_gate.py`。
- `prompt_nudge.sh` 初版：每回合一行 nudge，改寫自 fable-harness。
- `restore.sh` 初版；隨後新增 `agents/` 與 `hooks/` 還原迴圈，`hooks/*` 還原後補 `+x`。
