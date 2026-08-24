# 制度檔維護協議（按需）

<!-- 按需引用檔。想改 ~/.claude/ 下任何檔案前先讀本檔。
     變更歷史見 git 與 CHANGELOG.md：git log -p -- institution/rules-lib/maintenance.md -->

## 權限分級

| 級別 | 檔案 | 規則 |
|---|---|---|
| 自由改 | 各專案 `tasks/lessons.md`、`tasks/todo.md`、memory/ | 照 /lesson 與 memory 格式直接寫 |
| 可自行小改 | （目前無成員）——原唯一成員 `rules-lib/prompt-templates.md` 已於 2026-08-24 併入 `dispatch.md` | 先備份；只增修不重寫；改動理由寫進 commit message |
| 動前先問使用者 | `CLAUDE.md` 本體、`rules/hard-rules.md`、`rules/code-standards.md`、`rules-lib/` 下全部檔案、既有 skill 的鐵則段 | 弱模型只准「提議 diff＋理由」給使用者核准，不准直接改 |
| 不改 | backups/ | 歷史備份，只讀 |

未在上表明列的檔案或章節，一律預設為「動前先問使用者」。**新增的檔案預設進「動前先問」級**，
要降級須使用者明示。

## 改檔標準流程

1. `cp <檔> ~/.claude/backups/<檔名>.<YYYYMMDD>.bak`（`backup_gate.py` 會擋無備份的修改）
2. 用 Edit 做最小修改（不整檔重寫）
3. 改動理由寫進 commit message（Conventional Commits）；**不在檔尾加 Changelog 節**——
   常載與按需檔的變更歷史一律交還 git 與 repo 的 `CHANGELOG.md`（2026-08-14 檔頭改版
   原則，2026-08-24 延伸適用到所有制度檔）
4. 派 haiku fresh-context read-back：「這個改動有沒有跟 CLAUDE.md、rules/ 與 rules-lib/
   下任何檔案或三個 skill 打架？」（給它完整檔案清單）

## 踩雷教訓寫回哪裡

照 /lesson skill 執行（A 節記錄、B 節升級）；跨專案升級屬「動前先問」級 → 給使用者 diff。

## 加常載規則前必答兩題

想加一條常載規則之前，必答兩題：(1) 能不能做成 hook（機器強制）？(2) 能不能放進
按需引用檔或 skill（用時才載入）？兩題都答「不能」才准進常載檔。

## 精簡門檻（超過就行動）

| 對象 | 門檻 | 動作 |
|---|---|---|
| CLAUDE.md 本體 | 150 行 | 內容降級到 rules-lib/ 按需檔，本體只留路由行 |
| 常載合計（CLAUDE.md ＋ rules/ 下自動常載檔） | 200 行（對齊官方「target under 200 lines per CLAUDE.md file」） | 同上；或提議刪掉最少被觸發的規則 |
| 專案 tasks/lessons.md | 100 行 | 合併同類條目；已 promoted 的條目壓縮成一行 |
| rules-lib/ 單一按需檔 | 200 行 | 拆檔，CLAUDE.md 路由表加一行 |
| backups/ | 20 個檔 | 提議刪 3 個月前的備份（動前先問） |

計算行數時**扣掉 HTML 註解**（`<!-- -->` 區塊在注入 context 前會被剝除，不佔 token）。
另外跑內建 `/doctor`：它會列出 unused skills／MCP／plugins 與其 context 成本，並 flag
慢 hook——這是本表沒有的實測面。

## 過期檢查

- 發現任何規則與 harness 實際行為不符：不要默默繞過——記入 lessons.md 並回報使用者。
- 每次 Claude Code 大版本更新後，對照內建 system prompt 與官方文件覆核一次。
  **查證一律用 WebFetch／WebSearch 讀官方文件，不憑記憶**（hard-rules #8）。
- 覆核順序：**先問規則的『理由』是否仍成立，再問規則本身的『行為』是否仍成立**——
  兩者會分開過期，且理由通常先死。
  - 只有理由過期（規則行為仍對）→ 換理由，不動規則。2026-08-06 的 hard-rules #11 屬此類。
  - 連行為都被內建反轉 → **不自行選邊，回報使用者重新裁定**。2026-08-24 的 hard-rules #11
    屬此類：內建 Agent tool 說明已從「較貴的路徑」變成「Do not spawn agents unless the
    user asks」，同一條規則在兩次覆核裡走了兩種不同的處理。
- 逐條比對表與判定分類見 `docs/harness-overlap-2026-08.md`，該檔文末有重跑步驟。
