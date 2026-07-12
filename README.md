# claude-institution — 制度快照

這是 2026-07-05 一次性 Fable 5 session 建立的「Claude Code 跨專案制度」的**快照存檔**。

## 這是什麼、不是什麼

- **正本**在 `~/.claude/`（`CLAUDE.md`、`rules/`、`skills/`）與
  `~/.claude/projects/-Users-<username>-GitHub-claude-institution/memory/`。
  制度靠正本運作：每個新 session 由 `~/.claude/CLAUDE.md` 經 `@import` 載入常載規則。
- **本專案 `institution/` 是複製快照**，不是運作中的檔案。它的用途是：可攜、可版本控管
  （git）、可災難還原（`restore.sh`）。改快照不會影響任何 session；要改制度請改正本。

## 設計理念（一句話）

規則的強制力來自「放對層」，不是寫得多。機器可判定 → hook；每次必守的短規則 → 常載；
多步驟程序與範例 → 按需檔／skill；被糾正 → lessons.md，第 2 次觸發就升級固化。
讀者是較弱的模型，所以每條規則都力求「具體、可執行、有 if-then 判準與正反例」。

## 檔案清單（快照內容，共 29 檔）

### institution/CLAUDE.md
索引式主檔（≤150 行）：起手式、路由表、制度分層表，`@import` 兩個常載檔。

### institution/rules/（10 檔）
| 檔案 | 載入方式 | 內容 |
|---|---|---|
| `hard-rules.md` | 常載（@import） | 13 條硬規則：行為、調度、計畫、Git |
| `code-standards.md` | 常載（@import） | File Docstring 規範、Core Principles |
| `dispatch.md` | 按需 | 模型調度守則、型號表（2026-07-05 查證）、升降級路徑、驗證不自驗 |
| `judgment.md` | 按需 | 五個 rubric：升級／完成／問人／換路／品質底線，各附正反例 |
| `uplift.md` | 按需 | 判斷力增強協定：六個方法把單次直覺換成可檢驗流程 |
| `prompt-templates.md` | 按需 | 五種交辦範本：搜尋／實作／重構／研究／審查 |
| `diagnosis.md` | 按需 | 本 harness 三大耗損源與弱模型可照做的修法 |
| `maintenance.md` | 按需 | 制度檔維護：權限分級、精簡門檻、過期檢查 |
| `letter-to-future.md` | 按需 | 給未來 session 的交接信；含唯一未確認事項 |
| `final-assessment-fable5.md` | 按需 | 最後一個 Fable 5 session 的收尾評估與對抗審查結果（歷史文件，只讀） |

### institution/skills/（3 個 SKILL.md）
- `done-check` — 宣稱完成前的驗證 checklist，每個 ✅ 必附指令與輸出
- `lesson` — 被糾正後把教訓寫成 if-then 規則，含第 2 次觸發的升級程序
- `debug-protocol` — 系統化除錯 + 3-strike 停損規則

### institution/hooks/（5 檔，層 0 機器可判定規則）
借鑑自 Miguok/fable-harness 的同款機制，判斷邏輯保留、訊息改寫成指向本專案自己的規則；
不引入 fable 的 FABLE-PROTOCOL 命名或協定文字。
- `verify_gate.py` — Stop hook。本回合動了程式碼卻無測試指令 → 擋下並指向
  `hard-rules.md` #5 與 `/done-check`；fail-open，任何例外一律放行。
- `prompt_nudge.sh` — UserPromptSubmit hook。每回合一行提醒（指揮官不下場／
  /done-check／對抗審查），內容綁定本專案制度。
- `backup_gate.py` — PreToolUse hook（Edit/Write/NotebookEdit）。改動
  `~/.claude/` 制度檔前若今日無備份 → 擋下並提示備份指令；fail-open。
- `commit_guard.py` — PreToolUse hook（Bash git commit）。staged diff
  新增行含 console.log/debugger 等除錯碼 → 擋下；找不到 `git` 時 fail-open。
- `rm_guard.py` — PreToolUse hook（Bash rm/rmdir/find -delete）。命中
  `/`、`~`、`/Users/*` 等災難級路徑或未防呆的變數開頭遞迴刪除 → 擋下；
  fail-open（單一片段解析失敗且含 rm 時改保守 regex 擋，不直接放行）。

### institution/agents/（3 個對抗審查 subagent）
同樣借鑑自 fable-harness，指示改為引用 `rules/uplift.md` 方法 2（多答案評審）／
方法 3（對抗自查）。**正本放在 `~/.claude/agents/`，但該目錄已是第三方
`wshobson/agents` 的 git clone**——三個檔名已加進該 clone 的
`.git/info/exclude`，避免污染其 git status 或被 `git clean` 誤刪；
真正的還原保障是這份快照 + `restore.sh`。
- `skeptic.md` — 正確性鏡頭，預設「推翻它」，找邏輯漏洞與反例
- `red-team.md` — 安全／失效模式鏡頭，固定 5 項攻擊清單
- `simplifier.md` — 過度工程鏡頭，須提出實際簡化程式碼

### institution/memory/（3 檔）
- `institution-map.md` — 制度全貌，供 recall
- `MEMORY.md` — memory 索引
- `fable5-final-assessment.md` — 最終評估與收尾審查結果的位置指標（frontmatter 版，供 recall）

### institution/backups/（今日 4 個 .bak）
CLAUDE.md 的三個演進版本（Fable5 原版 → v2 路由化 → v3 加 uplift）與 letter-to-future 前一版。

## 執行需求（Python 與 git）

`institution/hooks/` 下的每個 `.py` hook 都以 `#!/usr/bin/env python3` 執行，需要：

- **Python 3.8 以上**（`backup_gate.py`、`commit_guard.py`、`verify_gate.py`、
  `rm_guard.py` 皆宣告 3.8+）。
- **僅用 Python 標準函式庫，不需要 `pip install` 任何套件**：實際用到的模組是
  `datetime / json / os / re / shlex / subprocess / sys / traceback`，全部內建。
- **`commit_guard.py` 額外需要 PATH 上有 `git`**；找不到 `git` 時該 hook
  fail-open（放行，不阻擋）。

**平台備註**：全新 macOS 在安裝 Xcode Command Line Tools 之前，`/usr/bin/python3`
只是個會提示安裝 CLT 的樁，不是可用的直譯器；多數 Linux 發行版預設已內建 python3。

**缺 Python 時會怎樣**：hook 無法執行，其防護即失效。但 `~/.claude/settings.json`
的 `permissions.deny` 規則（例如擋 `rm -rf /`、`rm -rf ~`）由 Claude Code 自身
解析，不經任何外部直譯器，即使 Python 不存在也照常生效——這層是不依賴 Python 的
最後防線。
（待確認：hook 因直譯器缺失而無法執行時，Claude Code 對非 0 非 2 exit code
的處理是否確實為「放行」而非「阻擋」，本專案尚未實測驗證。）

## 如何還原到 ~/.claude/

```bash
bash restore.sh
```

腳本會把 `institution/` 的 `CLAUDE.md`、`rules/`、三個 `skills/`、`agents/`、`hooks/`
複製回 `~/.claude/`，**覆寫前先把現有檔備份到 `~/.claude/backups/restore-<timestamp>/`**；
`hooks/` 還原後會自動補上可執行位元。
memory 因路徑含專案名、屬 project-scope，腳本只印提示、不自動覆寫。

## 唯一未確認事項

「被安全機制導向到 Opus 4.8 的請求是否消耗當前窗口額度」——本環境查不到，未確認。
建議到 claude.ai 的 usage 儀表板實測。詳見 `institution/rules/letter-to-future.md`。
（`@import` 是否於新 session 生效已於 2026-07-05 用 `claude -p` 實測確認。）
