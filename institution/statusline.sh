#!/bin/sh
#
# Claude Code statusLine 腳本：由 ~/.claude/settings.json 的 statusLine.command 呼叫，
# 每次畫面更新時從 stdin 收一份 session JSON，往 stdout 印一行狀態列。
# 存在的理由：額度與 context 用量是「用完才發現」的資源，把它們常駐在眼前，
# 才能在爆掉之前決定要不要 /compact 或換模型。
#
# 關鍵設計決策：
#   - 全用 $HOME / $cwd 推導路徑，不寫死任何個人化資訊，因此可隨預設流程還原
#     （不像 hooks/ 與 settings.json 需要 --with-hooks / --with-settings）。
#   - 用 POSIX sh 而非 bash：statusLine 每次更新都會啟動一次，啟動成本要最低。
#   - 讀不到的欄位一律留空並略過該區塊，不印 0% 或 unknown——寧可少一段，
#     不可印出會被誤讀為真實數值的預設值。
#
# Features:
#   - 目錄（$HOME 縮寫為 ~）＋ git branch（不在 repo 內則省略）
#   - model 顯示名稱、context 用量、5 小時與 7 天額度用量，各附 10 格文字進度條
#   - 進度條配色門檻：≤50% 綠、≤80% 黃、>80% 紅
#
# 已知極限:
#   - 依賴 jq；PATH 上沒有 jq 時所有欄位取值為空，只會印出目錄與 branch，
#     不會報錯也不會提示缺套件（statusLine 的錯誤訊息無處可顯示）。
#   - 額度與 context 欄位由 Claude Code 提供，欄位名稱隨版本可能變動；
#     變動時的表現是該區塊靜默消失，不是報錯。
#
# Dependencies:
#   - POSIX sh、jq、git（不在 repo 內時 git 失敗會被吞掉，不影響輸出）
#
input=$(cat)

cwd=$(echo "$input" | jq -r '.cwd // empty')
[ -z "$cwd" ] && cwd=$(pwd)

home="$HOME"
display_dir=$(echo "$cwd" | sed "s|^$home|~|")

git_branch=""
git -C "$cwd" rev-parse --git-dir > /dev/null 2>&1 && \
  git_branch=$(git -C "$cwd" symbolic-ref --short HEAD 2>/dev/null || git -C "$cwd" rev-parse --short HEAD 2>/dev/null)

model=$(echo "$input" | jq -r '.model.display_name // empty')

ESC=$(printf '\033')
C_GREEN="${ESC}[32m"
C_YELLOW="${ESC}[33m"
C_RED="${ESC}[31m"
C_DIM="${ESC}[2m"
C_RESET="${ESC}[0m"

make_bar() {
  pct=$1
  filled=$(( (pct + 5) / 10 ))
  [ $filled -gt 10 ] && filled=10
  [ $filled -lt 0 ] && filled=0
  empty=$((10 - filled))
  if [ "$pct" -le 50 ]; then
    color="$C_GREEN"
  elif [ "$pct" -le 80 ]; then
    color="$C_YELLOW"
  else
    color="$C_RED"
  fi
  bar="${color}"
  i=0; while [ $i -lt $filled ]; do bar="${bar}█"; i=$((i+1)); done
  bar="${bar}${C_RESET}${C_DIM}"
  i=0; while [ $i -lt $empty ]; do bar="${bar}░"; i=$((i+1)); done
  bar="${bar}${C_RESET}"
  printf '%s' "$bar"
}

five=$(echo "$input" | jq -r '.rate_limits.five_hour.used_percentage // empty')
week=$(echo "$input" | jq -r '.rate_limits.seven_day.used_percentage // empty')
rate_info=""
if [ -n "$five" ]; then
  five_int=$(printf '%.0f' "$five")
  rate_info="5h [$(make_bar "$five_int")] ${five_int}%"
fi
if [ -n "$week" ]; then
  week_int=$(printf '%.0f' "$week")
  rate_info="$rate_info  7d [$(make_bar "$week_int")] ${week_int}%"
fi
rate_info=$(echo "$rate_info" | sed 's/^  *//')

ctx_remaining=$(echo "$input" | jq -r '.context_window.remaining_percentage // empty')
ctx_info=""
if [ -n "$ctx_remaining" ]; then
  # 由 remaining 反推 used：欄位只保證有 remaining_percentage，
  # 不賭未經驗證的 used_percentage 欄位存在。
  ctx_used=$((100 - $(printf '%.0f' "$ctx_remaining")))
  ctx_info="ctx [$(make_bar "$ctx_used")] ${ctx_used}%"
fi

parts=""
[ -n "$model" ] && parts="$model"
if [ -n "$ctx_info" ]; then
  [ -n "$parts" ] && parts="$parts | $ctx_info" || parts="$ctx_info"
fi
if [ -n "$rate_info" ]; then
  [ -n "$parts" ] && parts="$parts  $rate_info" || parts="$rate_info"
fi
model_rate="$parts"

dir_part="\033[1;33m${display_dir}\033[0m"
[ -n "$git_branch" ] && dir_part="${dir_part} \033[34mgit:${git_branch}\033[0m"

if [ -n "$model_rate" ]; then
  printf "${dir_part}  \033[35m%s\033[0m" "$model_rate"
else
  printf "${dir_part}"
fi
