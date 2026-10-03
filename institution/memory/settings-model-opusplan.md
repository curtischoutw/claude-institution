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

事實：頂層 `"effortLevel": "high"` **對 Opus 5.5／Sonnet 5.5 不生效**（官方 settings-reference：
這一代的模型忽略 user 設定檔的頂層 key，只認 `modelSettings`），不設的話會落回預設 `medium`。
2026-10-03 起 `settings.json` 以 `modelSettings` 對 `claude-opus-5-5`、`claude-sonnet-5-5` 各設 `high`；
頂層 key 保留給 Opus 5、Fable 5.1 與更早的模型。若日後看到「effort 沒生效」，先查這裡。

相關：[[institution-map]]
