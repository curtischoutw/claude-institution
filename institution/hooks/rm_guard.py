#!/usr/bin/env python3
"""
PreToolUse hook（層 0，機器可判定規則）。攔 Bash：偵測 rm / rmdir /
find -delete 對「災難級路徑」的刪除並 block，防止一次失誤清空家目錄
或系統目錄。與 settings.json 的 permissions.deny 精確字串規則互為表裡：
deny 規則擋字面完全相同的指令，本 hook 負責語意變形（旗標順序、~ 與
$HOME 展開、相對路徑、glob、危險的變數寫法）。

「災難級路徑」定義（正規化後）：
  - `/` 本身
  - 任何深度 1 的絕對路徑（/Users、/tmp、/etc、/Library、/System…）
  - /Users/<任何人>（深度 2，含家目錄本身）、~、$HOME
  - 解析到上述位置的相對路徑與 `.`（依 hook 收到的 cwd 計算）
  - glob 尾綴指向上述位置（如 `rm -rf ~/*`、`rm -rf /*`）
  - 遞迴刪除中「未加防呆的變數開頭路徑」（如 `rm -rf $DIR/build`：
    變數意外為空即變成刪 /build）。安全寫法 `${DIR:?}/build` 或
    `${DIR:-預設}/build` 放行。

Features:
  - 展開 ~ 與 $HOME/${HOME}；相對路徑與 `.` 依 cwd 正規化後再判定；
    路徑比對 casefold（macOS APFS 大小寫不敏感，/USERS/<username> 也擋）。
  - 剝除 sudo/env/command/nohup/nice/time 包裝與前置變數賦值再認指令；
    一併剝除 shell 群組與流程控制的前導 token（{ } ! do then else），
    `{ rm -rf ~ ; }` 與 for/if 包裹的刪除不會逃檢。
  - 片段切割用 shlex punctuation 模式（引號感知，引號內的分號不誤切）；
    子 shell 括號內的指令（`(rm …)`）同樣納入檢查。
  - 內聯 shell 遞迴檢查：bash -c / sh -lc / eval 內的指令同樣受檢
    （深度上限 MAX_DEPTH，防套娃）。
  - find <路徑> … -delete 檢查起始路徑（-L/-H/-P/-O/-D 前置選項不影響
    認路徑）；-exec/-execdir 的子指令（到 ; 或 + 為止）遞迴受檢。
  - 清空級 glob 視同刪其上層目錄：basename 含 glob 字元（* ? [ {）且
    無字面前綴（如 /*、/.??*、/{.,}*）；窄 glob（lockfile*）不受影響。
  - 逐段追蹤 cd/pushd：「cd /Users && rm -rf <username>」用切換後的目錄
    解析相對路徑；cd 到變數等未知位置後，相對路徑放棄解析（fail-open）。
  - 誤判逃生口：指令內含 SKIP_RM_GUARD=1 即放行（寫 log 留痕供稽核）。
  - fail-open：stdin 解析失敗、內部錯誤 → 放行＋log（與其他 hook 一致）；
    但單一片段 shlex 解析失敗且含 rm 時，改用保守 regex 掃描不直接放行。

已知極限（誠實列出，勿當作全面保證）:
  - 擋不住「危險指令藏在被執行的腳本檔內」（bash foo.sh）。
  - 擋不住 xargs rm（目標來自 stdin，靜態分析看不到）。
  - 變數值在 hook 執行時未知，只能擋「危險寫法」不能擋「危險值」。
  - sudo -u <user> rm 這類帶參數的包裝可能漏認。
  - 已知誤擋（寧嚴勿鬆，接受）：rm -rf "~"（加引號的字面 ~ 檔名）
    會被當成家目錄擋下；shlex 剝殼後無法區分，真要刪用 ./~ 或逃生口。
  最後防線永遠是備份（Time Machine），本 hook 只降低機率。

Dependencies:
  - Python 3.8+（僅標準函式庫：datetime, json, os, re, shlex, sys, traceback）
"""

import datetime
import json
import os
import re
import shlex
import sys
import traceback

# ==============================
# 常數
# ==============================

LOG_PATH = os.path.expanduser("~/.claude/hooks/hooks.log")
HOME = os.path.realpath(os.path.expanduser("~"))

# 快篩：指令完全不含刪除動詞就直接放行，省解析成本
QUICK_RE = re.compile(r"\b(rm|rmdir|find)\b")

DELETE_CMDS = {"rm", "rmdir"}
WRAPPERS = {"sudo", "command", "env", "nohup", "nice", "time", "builtin"}
# shell 群組與流程控制的前導 token：剝掉才能認到真正的指令
# （{ rm … ; }、! rm …、for…do rm…、if…then rm…）
PREFIX_NOISE = {"{", "}", "!", "do", "then", "else"}
SHELL_CMDS = {"sh", "bash", "zsh", "dash", "ksh"}
ASSIGN_RE = re.compile(r"^\w+=")
MAX_DEPTH = 3  # 內聯 shell 遞迴檢查的深度上限

# glob 字元（含 brace expansion 的 {）
GLOB_CHARS = set("*?[{")
# 「清空整個目錄」級 glob 的第一字元：無字面前綴（* ? [ {）或 dotfile 掃法（.）
WIPE_GLOB_LEAD = ".*?[{"
_NO_CD = object()  # track_cd 的哨兵值：「這個片段不是 cd」

# 遞迴旗標：-r / -R / -rf / -fr / --recursive
RECURSIVE_FLAG_RE = re.compile(r"^-(-recursive$|[a-zA-Z]*[rR])")

# 未加防呆的變數開頭路徑：$VAR/... 或 ${VAR}/...（${VAR:?}、${VAR:-} 放行）
UNGUARDED_VAR_RE = re.compile(r"^\$(\w+|\{\w+\})/")

# shlex 解析失敗時的保守後援：rm 後面出現 / ~ $ 開頭的短目標就擋
FALLBACK_DANGER_RE = re.compile(
    r"\brm\b[^\n]*\s(/|~|\$HOME)(\s|$|/\*?\s|/\*?$)"
)

# 片段分隔 token（shlex punctuation_chars=True 的輸出）：含子 shell 括號
# 與重導向符（重導向目標被切成獨立無害片段，不影響判定）
SEPARATOR_CHARS = set("();<>|&")


def _log(line):
    """把一行事件寫入 LOG_PATH（best-effort；log 失敗絕不影響主流程）。

    Args:
        line: 要記錄的訊息（不含時間戳與元件名，本函式自加）。

    Returns:
        None。
    """
    try:
        ts = datetime.datetime.now().isoformat(timespec="seconds")
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"{ts} rm_guard: {line}\n")
    except Exception:
        pass


# ==============================
# 路徑判定
# ==============================

def expand_target(target, cwd):
    """展開 ~ / $HOME，並把相對路徑解析成絕對路徑。

    Args:
        target: shlex 解析後的單一目標 token（引號已去除）。
        cwd: hook 收到的執行目錄。

    Returns:
        str：正規化後的絕對路徑；無法解析的變數開頭路徑回傳 None。
    """
    t = target
    if t == "~" or t.startswith("~/"):
        t = HOME + t[1:]
    t = re.sub(r"^\$\{HOME\}", HOME, t)
    t = re.sub(r"^\$HOME(?=/|$)", HOME, t)
    if t.startswith("$"):
        return None  # 其他變數值未知，交給變數規則
    if not t.startswith("/"):
        if cwd is None:
            return None  # cd 到未知位置後的相對路徑，無從解析
        t = os.path.join(cwd, t)
    return os.path.normpath(t)


def is_protected_path(path):
    """判斷正規化後的絕對路徑是否為災難級路徑。

    比對一律先 casefold：macOS 預設 APFS 大小寫不敏感，
    /USERS/<username> 與 /Users/<username> 是同一個目錄。

    Args:
        path: 正規化後的絕對路徑。

    Returns:
        bool：True 表示該路徑不准刪。
    """
    p = path.casefold()
    if p == "/":
        return True
    parts = [x for x in p.split("/") if x]
    depth = len(parts)
    if depth == 1:
        return True
    if parts[0] == "users" and depth <= 2:
        return True
    if os.path.normpath(p) == HOME.casefold():
        return True
    return False


def check_target(target, cwd, recursive):
    """檢查單一刪除目標，回傳危險原因或 None。

    Args:
        target: 單一目標 token。
        cwd: 執行目錄。
        recursive: 該指令是否帶遞迴旗標（rmdir/find 視為 True）。

    Returns:
        str | None：危險原因說明；安全則 None。
    """
    if recursive and UNGUARDED_VAR_RE.match(target):
        var = target.split("/", 1)[0]
        return (
            f"目標「{target}」以未加防呆的變數開頭：{var} 意外為空時"
            f"會變成從根目錄刪起。請改用 ${{VAR:?}}/... 寫法"
        )
    expanded = expand_target(target, cwd)
    if expanded is None:
        return None
    base = os.path.basename(expanded)
    if base and (set(base) & GLOB_CHARS) and base[0] in WIPE_GLOB_LEAD:
        # 清空級 glob 尾綴（無字面前綴，如 /*、/.??*、/{.,}*）：
        # 視同刪其上層目錄。有字面前綴的窄 glob（lockfile*）不算。
        parent = os.path.dirname(expanded)
        if is_protected_path(parent):
            return f"目標「{target}」會清空受保護目錄 {parent}"
        return None
    if is_protected_path(expanded):
        return f"目標「{target}」解析為受保護路徑 {expanded}"
    return None


# ==============================
# 指令解析
# ==============================

def strip_wrappers(tokens):
    """剝除 sudo/env 等包裝指令與前置變數賦值。

    Args:
        tokens: shlex 解析出的 token 清單。

    Returns:
        list[str]：剝除後、以實際指令開頭的 token 清單。
    """
    toks = list(tokens)
    while toks and (
        toks[0] in WRAPPERS
        or toks[0] in PREFIX_NOISE
        or ASSIGN_RE.match(toks[0])
    ):
        toks.pop(0)
    return toks


def split_segments(command):
    """引號感知地把整串指令切成 token 片段清單。

    用 shlex punctuation 模式：引號內的 ; | & 不會被誤切
    （bash -c "cd / ; rm x" 的引號字串是完整單一 token）。

    Args:
        command: 完整指令字串。

    Returns:
        list[list[str]] | None：片段清單（每片段是 token 清單）；
        整串無法解析（引號不平衡等）回傳 None 交呼叫端保守處理。
    """
    lex = shlex.shlex(command.replace("\n", ";"), posix=True,
                      punctuation_chars=True)
    lex.whitespace_split = True
    try:
        tokens = list(lex)
    except ValueError:
        return None
    segments, cur = [], []
    for t in tokens:
        if t and set(t) <= SEPARATOR_CHARS:
            if cur:
                segments.append(cur)
                cur = []
        else:
            cur.append(t)
    if cur:
        segments.append(cur)
    return segments


def track_cd(tokens, cwd):
    """若片段是 cd/pushd，回傳切換後的有效 cwd；否則回傳 _NO_CD。

    Args:
        tokens: 單一片段的 token 清單。
        cwd: 目前的有效 cwd（可為 None＝未知）。

    Returns:
        str | None | _NO_CD：新 cwd（None 表示切到未知位置）；
        非 cd 片段回傳哨兵 _NO_CD。
    """
    toks = strip_wrappers(tokens)
    if not toks or toks[0] not in ("cd", "pushd"):
        return _NO_CD
    args = [t for t in toks[1:] if not t.startswith("-")]
    if not args:
        return HOME  # 裸 cd 回家目錄
    return expand_target(args[0], cwd)  # 變數/未知 → None


def check_command(command, cwd, depth=0):
    """把整串指令切成片段逐段檢查(含內聯 shell 的遞迴進入點)。

    逐段追蹤 cd/pushd，讓「cd /Users && rm -rf <username>」這種
    相對路徑刪除用切換後的目錄解析。

    Args:
        command: 完整指令字串。
        cwd: 執行目錄。
        depth: 目前遞迴深度（防 bash -c 無限套娃）。

    Returns:
        str | None：危險原因；安全則 None。
    """
    if depth > MAX_DEPTH:
        return None
    segments = split_segments(command)
    if segments is None:
        # 解析不了又含 rm：保守 regex 後援，不直接放行
        if FALLBACK_DANGER_RE.search(command):
            return f"無法解析的指令疑似對根/家目錄執行 rm：{command[:80]}"
        return None
    eff_cwd = cwd
    for toks in segments:
        new_cwd = track_cd(toks, eff_cwd)
        if new_cwd is not _NO_CD:
            eff_cwd = new_cwd
            continue
        reason = check_segment(toks, eff_cwd, depth)
        if reason:
            return reason
    return None


def check_segment(tokens, cwd, depth=0):
    """檢查單一指令片段（token 清單），回傳危險原因或 None。

    Args:
        tokens: 單一片段的 token 清單（split_segments 的輸出）。
        cwd: 執行目錄。
        depth: 目前遞迴深度。

    Returns:
        str | None：危險原因；安全則 None。
    """
    toks = strip_wrappers(tokens)
    if not toks:
        return None
    cmd = os.path.basename(toks[0])

    if cmd in DELETE_CMDS:
        recursive = cmd == "rmdir" or any(
            RECURSIVE_FLAG_RE.match(t) for t in toks[1:]
        )
        seen_ddash = False
        for t in toks[1:]:
            if t == "--":
                seen_ddash = True
                continue
            if not seen_ddash and t.startswith("-") and t != "-":
                continue
            reason = check_target(t, cwd, recursive)
            if reason:
                return reason
        return None

    # 內聯 shell（bash -c / sh -lc …）：把 -c 後的字串遞迴檢查
    if cmd in SHELL_CMDS:
        saw_c_flag = False
        for t in toks[1:]:
            if t.startswith("-") and "c" in t[1:]:
                saw_c_flag = True
                continue
            if saw_c_flag and not t.startswith("-"):
                return check_command(t, cwd, depth + 1)
        return None

    # eval：把其餘引數併回一串指令遞迴檢查
    if cmd == "eval" and len(toks) > 1:
        return check_command(" ".join(toks[1:]), cwd, depth + 1)

    if cmd == "find" and any(
        f in toks for f in ("-delete", "-exec", "-execdir")
    ):
        # 跳過 find 的合法前置選項（-L/-H/-P/-O?/-D <debugopts>），
        # 它們出現在起始路徑之前，不能當作「表達式開始」提早 break
        i = 1
        while i < len(toks):
            t = toks[i]
            if t in ("-L", "-H", "-P") or t.startswith("-O"):
                i += 1
            elif t == "-D":
                i += 2
            else:
                break
        for t in toks[i:]:
            if t.startswith(("-", "(", "!")):
                break  # find 的表達式開始，路徑參數結束
            reason = check_target(t, cwd, recursive=True)
            if reason:
                return reason
        # -exec/-execdir 的子指令（到 ; 或 + 為止）也要檢查
        for flag in ("-exec", "-execdir"):
            if flag not in toks:
                continue
            idx = toks.index(flag) + 1
            sub = []
            while idx < len(toks) and toks[idx] not in (";", "+"):
                sub.append(toks[idx])
                idx += 1
            if sub:
                reason = check_command(" ".join(sub), cwd, depth + 1)
                if reason:
                    return reason
    return None


# ==============================
# 主流程
# ==============================

def main():
    """PreToolUse 進入點。放行 exit 0；阻擋 exit 2＋stderr 說明。

    Args:
        （無；讀 stdin）

    Returns:
        int：0 放行、2 阻擋。
    """
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
        tool_input = data.get("tool_input") or {}
        command = tool_input.get("command") or ""

        if not QUICK_RE.search(command):
            return 0
        if "SKIP_RM_GUARD=1" in command:
            _log(f"SKIP 逃生口被使用: {command[:120]}")
            return 0

        cwd = data.get("cwd") or os.getcwd()
        reason = check_command(command, cwd)
        if reason:
            _log(f"BLOCK {reason} | 指令: {command[:120]}")
            sys.stderr.write(
                "[rm_guard] 阻擋危險刪除。\n"
                f"原因：{reason}\n"
                "這條 hook 保護根目錄、系統目錄與家目錄不被整個刪除。\n"
                "若確認是誤判，先向使用者說明，經同意後在指令前加 "
                "SKIP_RM_GUARD=1 重跑（會留 log 供稽核）。\n"
            )
            return 2
        return 0
    except Exception:
        # fail-open：hook 本身出任何錯都不可以擋住正常工作；但要留痕。
        _log("ERROR " + traceback.format_exc().replace("\n", " | "))
        return 0


if __name__ == "__main__":
    sys.exit(main())
