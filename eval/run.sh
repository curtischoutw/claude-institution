#!/bin/zsh
# eval/run.sh — 制度 eval 執行器：對 t3–t6 跑「有制度（A）」或「零制度（C）」，並驗證條件確實不同。
#
# 為什麼存在：2026-10-03 第一輪 eval 在 Claude Code session 內用 `claude -p` 啟動子 session，
# 子 session 繼承了 CLAUDE_CODE_SAFE_MODE=1／CLAUDE_CODE_DISABLE_CLAUDE_MDS=1，「有制度」組悄悄
# 變成零制度，整輪作廢。本腳本把「預檢環境」與「跑完檢查制度確實載入」做成機器強制。
#
# 用法：
#   bash eval/run.sh A [t3 t4 t5 t6]        # 有制度；預設四題，t3/t4 跑 1 次、t5 2 次、t6 3 次
#   bash eval/run.sh C [t3 t4 t5 t6]        # 零制度（--safe-mode）
#   bash eval/run.sh check <A|C> <out_dir>  # 只做載入檢查（跑完後想重驗時用）
# 環境變數：EVAL_OUT（輸出目錄，預設 ${TMPDIR:-/tmp}/eval-<日期>-<組別>）、EVAL_N（所有題統一跑幾次）
#
# Features:
#   - 每題獨立沙盒（t3/t4 複製 eval/fixtures，不動 repo 內的 fixture）；prompt 直接取自 eval/tasks/*.md
#   - 預檢：A 組若環境帶 safe mode 變數就拒絕執行，不建立任何輸出
#   - 載入檢查：A 組每個 run 的 skill 清單必須含 verify；C 組必須不含——否則明說「結果不可用」
#   - 兩組旗標相同，只差 C 組的 --safe-mode；不使用 --dangerously-skip-permissions
#
# 已知極限：
#   - 必須在「正常終端機」執行，不能在 Claude Code session 內（見上）。
#   - 只做執行與條件檢查，不評分；評分流程（盲評、全部 assistant 文字）見 eval/README.md。
#   - 載入檢查靠 transcript 的 skill_listing 附件，Claude Code 日後改格式時需同步改本檔。
#   - 本機有 macOS 的 zsh 與 perl 才能跑（alarm 當 timeout，macOS 沒有 timeout 指令）。
#
# Dependencies: zsh、claude CLI、perl、python3（皆為系統內建或已安裝）

[ -n "$ZSH_VERSION" ] || exec zsh "$0" "$@"   # 本檔用 zsh 語法；被 bash／sh 呼叫時自動切換

REPO=${0:A:h:h}

# ==============================
# 載入檢查
# ==============================

# check_loaded <A|C> <out_dir>：逐個 run 檢查制度載入狀態是否符合該組預期。
# Args: 組別（A 應載入、C 應未載入）、輸出目錄。 Returns: 0＝全部符合；1＝有 run 不符或找不到。
check_loaded() {
  python3 - "$1" "$2" <<'EOF'
import glob, json, os, re, sys
group, out = sys.argv[1], sys.argv[2].rstrip("/")
dirs = sorted(d for d in glob.glob(out + "/*/") if os.path.isdir(d + "sandbox"))
if not dirs:
    print("找不到任何 run 目錄：" + out); sys.exit(1)
enc = lambda p: re.sub(r"[^A-Za-z0-9]", "-", p)       # Claude Code 把路徑編成 projects/ 下的目錄名
want = group == "A"
bad = 0
for d in dirs:
    name = os.path.basename(d.rstrip("/"))
    cands = glob.glob(os.path.expanduser(f"~/.claude/projects/{enc(d + 'sandbox')}/*.jsonl"))
    if not cands:  # 沙盒路徑編碼不同時，退回用尾段比對
        cands = glob.glob(os.path.expanduser(f"~/.claude/projects/*{enc(os.path.basename(out) + '/' + name + '/sandbox')}/*.jsonl"))
    if not cands:
        print(f"{name}: 找不到 transcript"); bad += 1; continue
    loaded = False
    for line in open(cands[0], encoding="utf-8", errors="replace"):
        try: e = json.loads(line)
        except Exception: continue
        a = e.get("attachment", {}) if e.get("type") == "attachment" else {}
        if a.get("type") == "skill_listing" and re.search(r"^- verify:", a.get("content", ""), re.M): loaded = True
        if a.get("type") == "session_context" and "claudeMd" in (a.get("context") or {}): loaded = True
    ok = loaded == want
    bad += 0 if ok else 1
    print(f"{name}: {'OK  ' if ok else '不符'}  制度載入={loaded}（{group} 組預期 {want}）")
print("\n結論：" + ("條件確實如預期，結果可用" if not bad else f"{bad} 個 run 條件不符或找不到——結果不可用，先檢查環境變數與 ~/.claude"))
sys.exit(1 if bad else 0)
EOF
}

# ==============================
# 單一 run（由 xargs 平行呼叫）
# ==============================

# run_job <A|C> <task> <n>：建沙盒、擷取 prompt、執行 claude -p，結果寫入 <out>/<task>-<組別>-<n>/。
run_job() {
  local g=$1 t=$2 n=$3 out=${EVAL_OUT:?} D tf
  D=$out/$t-$g-$n; rm -rf $D; mkdir -p $D/sandbox
  case $t in t3|t4) mkdir -p $D/sandbox/eval && cp -R $REPO/eval/fixtures $D/sandbox/eval/fixtures ;; esac
  tf=$(ls $REPO/eval/tasks/$t-*.md | head -1)
  awk '/^## 任務 prompt/{f=1;next} f&&/^```/{c++; if(c==2)exit; next} f&&c==1{print}' $tf > $D/prompt.txt
  [ -s $D/prompt.txt ] || { echo "exit=prompt-empty" > $D/done.txt; return 1; }
  local flags=(-p --model opus --effort high --add-dir $HOME/.claude)   # --add-dir：讓 A 組讀得到 rules-lib
  case $t in t3|t4) flags+=(--permission-mode acceptEdits --allowedTools "Read" "Edit" "Write" "Glob" "Grep"
                            "Bash(python3 *)" "Bash(cd *)" "Bash(diff *)" "Bash(cat *)" "Bash(ls *)") ;; esac
  [ $g = C ] && flags+=(--safe-mode)
  cd $D/sandbox
  perl -e 'alarm 1500; exec @ARGV' claude "${flags[@]}" < $D/prompt.txt > $D/answer.md 2> $D/stderr.txt
  echo "exit=$?" > $D/done.txt
}

# ==============================
# 進入點
# ==============================

case $1 in
  job) shift; run_job "$@"; exit 0 ;;
  check) check_loaded "$2" "$3"; exit $? ;;
  A|C) ;;
  *) sed -n '/^# 用法/,/^# 環境變數/p' $0; exit 2 ;;
esac

G=$1; shift
TASKS=(${@:-t3 t4 t5 t6})

# 預檢（A 組）：子 session 會繼承這些變數，A 組就載不到制度
bad=0
if [ $G = A ]; then
  for v in CLAUDE_CODE_SAFE_MODE CLAUDE_CODE_DISABLE_CLAUDE_MDS CLAUDE_CODE_CHILD_SESSION; do
    [ -n "${(P)v}" ] && { echo "✗ 環境變數 $v 有設定（值=${(P)v}），子 session 會繼承，A 組將無法載入制度。"; bad=1; }
  done
  [ -e $HOME/.claude/skills/verify/SKILL.md ] || { echo "✗ 找不到 ~/.claude/skills/verify/SKILL.md，A 組沒有制度可載入"; bad=1; }
fi
command -v claude >/dev/null || { echo "✗ 找不到 claude 指令"; bad=1; }
for t in $TASKS; do ls $REPO/eval/tasks/$t-*.md >/dev/null 2>&1 || { echo "✗ 找不到題目 $t"; bad=1; }; done
if [ $bad = 1 ]; then echo "\n預檢失敗，未執行任何 run。請開新的終端機視窗（不是 Claude Code 內）再試。"; exit 1; fi

export EVAL_OUT=${EVAL_OUT:-${TMPDIR:-/tmp}/eval-$(date +%Y%m%d)-$G}
mkdir -p $EVAL_OUT
declare -A RUNS=(t3 1 t4 1 t5 2 t6 3)
jobs=""
for t in $TASKS; do for ((i=1; i<=${EVAL_N:-${RUNS[$t]:-1}}; i++)); do jobs+="job $G $t $i\n"; done; done
echo "預檢通過：claude $(claude --version 2>&1 | head -1)；$G 組 $(printf "$jobs" | wc -l | tr -d ' ') 個 run，輸出 $EVAL_OUT"
printf "$jobs" | xargs -P 4 -L 1 zsh $0

echo "\n== 完成狀態 =="
for d in $EVAL_OUT/*/; do echo "$(basename $d): $(cat $d/done.txt 2>/dev/null || echo 未完成)  answer=$(wc -c < $d/answer.md 2>/dev/null)B"; done
echo "\n== 載入檢查 =="
check_loaded $G $EVAL_OUT
