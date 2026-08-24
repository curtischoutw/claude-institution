#!/bin/sh
# UserPromptSubmit hook（層 0）。每個 user turn 開始時，往 stdout 印一行
#   提醒，內容綁定本專案自己的制度（/done-check / 派工是例外 / 對抗審查），
#   不是 fable-harness 原版的 FABLE-PROTOCOL 文字。
#
#   設計取材自 Miguok/fable-harness 的 prompt_nudge.sh（同款「每回合一行
#   nudge」機制），但訊息全部改寫為指向 ~/.claude/skills/done-check、
#   ~/.claude/rules-lib/dispatch.md、~/.claude/rules-lib/uplift.md 方法 2/3，
#   避免引入重複的協定文字。
#
#   2026-08-24：nudge 文字隨 hard-rules #11 改條件式同步重寫。舊版寫
#   「指揮官不下場（讀>3檔/搜尋/掃repo/批次改/驗證都派 subagent）」，
#   與內建 Agent tool 說明「Do not spawn agents unless the user asks…
#   handle it inline」對撞；每回合注入一句與內建牴觸的話比不注入更糟。
#
# Features:
#   - 單行輸出，不做任何判斷邏輯，成本極低。
#   - 無 exit 處理即代表 fail-open（腳本本身出錯不會擋住 session）。
#
# Dependencies:
#   - POSIX sh

echo "🧭 宣稱完成前走 /done-check 並附實際指令與輸出；派 subagent 是例外（只在中間輸出會淹沒主 context 或需 fresh-context 驗證時）；重大結論先用 /code-review、/simplify、/security-review。"
