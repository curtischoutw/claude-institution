# claude-institution — 我的 Claude Code 最小設定

開發流程交給 plugin：**mattpocock-skills** 管流程（問什麼、何時寫 spec、切票、審查），
**ws（claude-code-workflows）** 管領域專業（語言與領域型 agent）。本 repo 只保留這兩者
補不到的少數幾件事。

> 2026-10-24 以前這裡是一套有分層規則、skill、四個 hook 的完整制度；因為用不到而縮到現在這樣。
> 舊版留在 git 歷史（最後完整版：commit `7a409e6`），`~/.claude/backups/` 也有打包檔。

## 現在留下的東西

`institution/` 是 `~/.claude/` 的**複製快照**（正本在 `~/.claude/`），用途是可攜與災難還原。

| 檔案 | 做什麼 |
|---|---|
| `CLAUDE.md` | 常載。路由（除錯、新功能、審查各去哪）＋派工規則：情境對應的 agent 類型與模型、必指定 `model`、升降級、派工包範本、驗證不自驗 |
| `rules/code-standards.md` | 常載。原始碼檔頭怎麼寫（不寫作者／日期／版本）＋安全底線（輸入驗證、secret、參數化、新增依賴先問） |
| `rules-lib/uplift.md` | 情境載入（`CLAUDE.md` 路由到它）。高風險判斷用的 6 個方法：先寫判準、多答案評審、紅隊自查、結論要能被證偽、決策日誌、問題重述 |
| `hooks/rm_guard.py` | PreToolUse hook。擋下會清空家目錄或系統目錄的 `rm`／`rmdir`／`find -delete`（含 `~`、`$HOME`、glob、未防呆的變數路徑） |
| `settings.json` | 快照（去識別化）：`permissions.deny` 的 rm 規則、`rm_guard` 綁定、plugin 與 marketplace、model 設定 |
| `statusline.sh` | 狀態列腳本 |

## 還原

```bash
bash restore.sh --dry-run          # 先看會動哪些檔
bash restore.sh                    # 還原 CLAUDE.md、rules/、rules-lib/、statusline.sh
bash restore.sh --with-hooks       # 另外還原 hooks/
bash restore.sh --with-settings    # 另外還原 settings.json（<username> 會換成 whoami）
```

覆寫前會先備份到 `~/.claude/backups/restore-<timestamp>/`。`hooks/` 與 `settings.json`
預設略過，因為快照是去識別化版本。

## 刪掉之後要知道的事

- 沒有 `commit_guard`：mattpocock 的 `/implement` 最後會自動 commit，不再有除錯碼檢查。
- 沒有 `/verify` 與 `verify_gate`：「宣稱完成要附實際指令輸出」不再強制。
- 沒有派工「閘門」：plan mode 照內建流程派 Explore／Plan agent。
- 沒有誠實條款與不可逆動作前引原話的規定：改靠內建指引。

## 其他

- `docs/plugin-guide.md` — 已安裝 plugin 的用途、指令與注意事項（plugin 升版後可能不準）。
- `docs/mattpocock-skills-guide.html`、`docs/mattpocock-ws-workflow.html` — 兩個 plugin 的操作步驟卡。
- `CHANGELOG.md` — repo 層級變更。
