# 制度檔維護協議

<!-- 按需引用檔。想改 ~/.claude/ 下任何檔案前先讀本檔。建立：2026-07-05（Fable 5 session）。 -->

## 權限分級

| 級別 | 檔案 | 規則 |
|---|---|---|
| 自由改 | 各專案 `tasks/lessons.md`、`tasks/todo.md`、memory/ | 照 /lesson 與 memory 格式直接寫 |
| 可自行小改 | `rules-lib/prompt-templates.md` | 先備份；只增修不重寫；檔尾 Changelog 加一行（日期＋改了什麼＋為什麼） |
| 動前先問使用者 | `CLAUDE.md` 本體、`rules/hard-rules.md`、`rules/code-standards.md`、`rules-lib/judgment.md`、`rules-lib/maintenance.md`（本檔）、既有 skill 的鐵則段 | 弱模型只准「提議 diff＋理由」給使用者核准，不准直接改 |
| 不改 | backups/ | 歷史備份，只讀 |

未在上表明列的檔案或章節，一律預設為「動前先問使用者」。

## 改檔標準流程（可自行小改級）

1. `cp <檔> ~/.claude/backups/<檔名>.<YYYYMMDD>.bak`
2. 用 Edit 做最小修改（不整檔重寫）
3. 檔尾 Changelog 加一行
4. 派 haiku fresh-context read-back：「這個改動有沒有跟 CLAUDE.md、rules/ 與 rules-lib/
   下任何檔案或三個 skill 打架？」（給它完整檔案清單）

## 踩雷教訓寫回哪裡

照 /lesson skill 執行（A 節記錄、B 節升級）；跨專案升級屬「動前先問」級 → 給使用者 diff。

## 加常載規則前必答兩題

想加一條常載規則之前，必答兩題：(1) 能不能做成 hook（機器強制）？(2) 能不能放進
按需引用檔或 skill（用時才載入）？兩題都答「不能」才准進常載檔（2026-08-06 自
`diagnosis.md` 併入，該檔原是純指標檔，功能已被本節與 CLAUDE.md 路由表取代而刪除）。

## 精簡門檻（超過就行動）

| 對象 | 門檻 | 動作 |
|---|---|---|
| CLAUDE.md 本體 | 150 行 | 內容降級到 rules-lib/ 按需檔，本體只留路由行 |
| 常載合計（CLAUDE.md ＋ rules/ 下自動常載檔） | 200 行（2026-08-06 由 500 行下修，對齊官方 CLAUDE.md 建議上限） | 同上；或提議刪掉最少被觸發的規則 |
| 專案 tasks/lessons.md | 100 行 | 合併同類條目；已 promoted 的條目壓縮成一行 |
| rules-lib/ 單一按需檔 | 200 行 | 拆檔，CLAUDE.md 路由表加一行 |
| backups/ | 20 個檔 | 提議刪 3 個月前的備份（動前先問） |

## 過期檢查

- 發現任何規則與 harness 實際行為不符：不要默默繞過——記入 lessons.md 並回報使用者。
- 每次 Claude Code 大版本更新後，對照內建 system prompt 覆核一次；**先問規則的
  『理由』是否仍成立，不是只問『這條規則還要不要』**——規則過期常先從動機開始
  （見 hard-rules #11 的實例：規則本身仍成立，但「省額度」的理由已被平台計價方式
  反轉，2026-08-06）。

## Changelog

- 2026-08-06：`diagnosis.md` 刪檔後併入本檔「加常載規則前必答兩題」節；精簡門檻
  「常載合計」500→200 行；過期檢查加「先問理由是否仍成立」一句。詳見
  docs/harness-overlap-2026-08.md（使用者核准）。
- 2026-07-05：初版（Fable 5 session）。
- 2026-07-13：制度精簡（Fable 5 審查，使用者核准）——權限表移除已刪檔條目；
  踩雷節去重改引用 /lesson；型號表過期檢查隨 dispatch.md 靜態表一併移除。
- 2026-07-26：rules 按需檔移至 rules-lib/（脫離新版 Claude Code 對 rules/ 的自動常載），路徑引用同步更新（/doctor 健檢，使用者核准）。
