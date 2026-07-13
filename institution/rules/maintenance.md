# 制度檔維護協議

<!-- 按需引用檔。想改 ~/.claude/ 下任何檔案前先讀本檔。建立：2026-07-05（Fable 5 session）。 -->

## 權限分級

| 級別 | 檔案 | 規則 |
|---|---|---|
| 自由改 | 各專案 `tasks/lessons.md`、`tasks/todo.md`、memory/ | 照 /lesson 與 memory 格式直接寫 |
| 可自行小改 | `rules/prompt-templates.md`、`rules/diagnosis.md`、`rules/dispatch.md` 的「可用型號」表 | 先備份；只增修不重寫；檔尾 Changelog 加一行（日期＋改了什麼＋為什麼） |
| 動前先問使用者 | `CLAUDE.md` 本體、`rules/hard-rules.md`、`rules/code-standards.md`、`rules/judgment.md`、`rules/maintenance.md`（本檔）、既有 skill 的鐵則段 | 弱模型只准「提議 diff＋理由」給使用者核准，不准直接改 |
| 不改 | backups/ | 歷史備份，只讀 |

未在上表明列的檔案或章節，一律預設為「動前先問使用者」。

## 改檔標準流程（可自行小改級）

1. `cp <檔> ~/.claude/backups/<檔名>.<YYYYMMDD>.bak`
2. 用 Edit 做最小修改（不整檔重寫）
3. 檔尾 Changelog 加一行
4. 派 haiku fresh-context read-back：「這個改動有沒有跟 CLAUDE.md、rules/ 下任何檔案
   或三個 skill 打架？」（給它完整檔案清單）

## 踩雷教訓寫回哪裡

- 一律先進當前專案的 `tasks/lessons.md`（格式照 /lesson skill，含 if-then 判準）。
- 跨專案通用的教訓：在 lessons.md 記錄後，另外「提議」升級進 hard-rules.md 或對應 skill
  （動前先問級 → 給使用者 diff）。機器可判定的 → 提議做成 hook（/update-config）。

## 精簡門檻（超過就行動）

| 對象 | 門檻 | 動作 |
|---|---|---|
| CLAUDE.md 本體 | 150 行 | 內容降級到 rules/ 按需檔，本體只留路由行 |
| 常載合計（本體＋@import 檔） | 500 行 | 同上；或提議刪掉最少被觸發的規則 |
| 專案 tasks/lessons.md | 100 行 | 合併同類條目；已 promoted 的條目壓縮成一行 |
| rules/ 單一按需檔 | 200 行 | 拆檔，CLAUDE.md 路由表加一行 |
| backups/ | 20 個檔 | 提議刪 3 個月前的備份（動前先問） |

## 過期檢查

- `dispatch.md` 的型號表帶有查證日期：距今超過約 3 個月又要引用時，先派 claude-code-guide
  重新查證，再照「可自行小改」流程更新。
- 發現任何規則與 harness 實際行為不符：不要默默繞過——記入 lessons.md 並回報使用者。

## Changelog

- 2026-07-05：初版（Fable 5 session）。
