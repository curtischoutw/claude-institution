---
name: settings-model-opusplan
description: 使用者的 Claude Code model 設定是 opusplan，不是 opus；快照與家目錄不一致時以此為準
metadata: 
  node_type: memory
  type: user
  originSessionId: 53bf0fcd-7415-465c-bf7c-b16ee3dd8296
  modified: 2026-08-24T15:43:03.388Z
---

使用者 `~/.claude/settings.json` 的 `"model"` 意圖值是 **`"opusplan"`**（2026-08-24 明確
裁定：「我的 Model 就是要 opusplan」）。

2026-08-24 我曾看到快照是 `opusplan`、家目錄是 `opus`，用 mtime 推斷「家目錄較新＝正解」，
開 PR 把快照改成 `opus`，方向完全相反（PR #11 已合併後由 PR #12 revert）。若日後再遇到
兩邊 `model` 不一致，`opusplan` 是使用者要的那個，另一邊才是待修正的。

更通用的判準（不限 model 欄位）已記入 repo 的 `tasks/lessons.md`：設定值兩邊不同時，
mtime 只能說明「誰後寫」，不能說明「誰對」——回報雙方值與先後，請使用者裁定。

相關：[[institution-map]]
