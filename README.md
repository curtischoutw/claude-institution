# fable_once — 制度快照

這是 2026-07-05 一次性 Fable 5 session 建立的「Claude Code 跨專案制度」的**快照存檔**。

## 這是什麼、不是什麼

- **正本**在 `~/.claude/`（`CLAUDE.md`、`rules/`、`skills/`）與
  `~/.claude/projects/-Users-curtis-GitHub-fable-once/memory/`。
  制度靠正本運作：每個新 session 由 `~/.claude/CLAUDE.md` 經 `@import` 載入常載規則。
- **本專案 `institution/` 是複製快照**，不是運作中的檔案。它的用途是：可攜、可版本控管
  （git）、可災難還原（`restore.sh`）。改快照不會影響任何 session；要改制度請改正本。

## 設計理念（一句話）

規則的強制力來自「放對層」，不是寫得多。機器可判定 → hook；每次必守的短規則 → 常載；
多步驟程序與範例 → 按需檔／skill；被糾正 → lessons.md，第 2 次觸發就升級固化。
讀者是較弱的模型，所以每條規則都力求「具體、可執行、有 if-then 判準與正反例」。

## 檔案清單（快照內容，共 19 檔）

### institution/CLAUDE.md
索引式主檔（≤150 行）：起手式、路由表、制度分層表，`@import` 兩個常載檔。

### institution/rules/（9 檔）
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

### institution/skills/（3 個 SKILL.md）
- `done-check` — 宣稱完成前的驗證 checklist，每個 ✅ 必附指令與輸出
- `lesson` — 被糾正後把教訓寫成 if-then 規則，含第 2 次觸發的升級程序
- `debug-protocol` — 系統化除錯 + 3-strike 停損規則

### institution/memory/（2 檔）
- `institution-map.md` — 制度全貌，供 recall
- `MEMORY.md` — memory 索引

### institution/backups/（今日 4 個 .bak）
CLAUDE.md 的三個演進版本（Fable5 原版 → v2 路由化 → v3 加 uplift）與 letter-to-future 前一版。

## 如何還原到 ~/.claude/

```bash
bash restore.sh
```

腳本會把 `institution/` 的 `CLAUDE.md`、`rules/`、三個 `skills/` 複製回 `~/.claude/`，
**覆寫前先把現有檔備份到 `~/.claude/backups/restore-<timestamp>/`**。
memory 因路徑含專案名、屬 project-scope，腳本只印提示、不自動覆寫。

## 唯一未確認事項

「被安全機制導向到 Opus 4.8 的請求是否消耗當前窗口額度」——本環境查不到，未確認。
建議到 claude.ai 的 usage 儀表板實測。詳見 `institution/rules/letter-to-future.md`。
（`@import` 是否於新 session 生效已於 2026-07-05 用 `claude -p` 實測確認。）
