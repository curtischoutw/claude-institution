#!/bin/sh
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
  ctx_int=$(printf '%.0f' "$ctx_remaining")
  ctx_info="ctx [$(make_bar "$ctx_int")] ${ctx_int}%"
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
