#!/bin/sh
# File: prompt_nudge.sh
# Author: Curtis Chou
# Email: <your-email>
# Created Date: 2026-07-05
# Version: 1.0.0
# Copyright (c) 2026 Curtis Chou
#
# Description:
#   UserPromptSubmit hook（層 0）。每個 user turn 開始時，往 stdout 印一行
#   提醒，內容綁定本專案自己的制度（指揮官不下場 / /done-check / 對抗審查），
#   不是 fable-harness 原版的 FABLE-PROTOCOL 文字。
#
#   設計取材自 Miguok/fable-harness 的 prompt_nudge.sh（同款「每回合一行
#   nudge」機制），但訊息全部改寫為指向 ~/.claude/rules-lib/dispatch.md、
#   ~/.claude/skills/done-check、~/.claude/rules-lib/uplift.md 方法 2/3，
#   避免引入重複的協定文字（原引用 diagnosis.md 第 2 名：常載膨脹，該檔
#   2026-08-06 已刪並併入 ~/.claude/rules-lib/maintenance.md）。
#
# Features:
#   - 單行輸出，不做任何判斷邏輯，成本極低。
#   - 無 exit 處理即代表 fail-open（腳本本身出錯不會擋住 session）。
#
# Dependencies:
#   - POSIX sh
#
# Version History:
#   1.0.0 (2026-07-05): 初版，改寫自 fable-harness prompt_nudge.sh。

echo "🧭 指揮官不下場（讀>3檔/搜尋/掃repo/批次改/驗證都派 subagent）；宣稱完成前走 /done-check 並附實際指令與輸出；重大結論可派 skeptic/red-team/simplifier 做對抗審查。"
