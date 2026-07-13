#!/usr/bin/env python3
"""
File: commit_guard.py
Author: Curtis Chou
Email: <your-email>
Created Date: 2026-07-06
Version: 1.0.0
Copyright (c) 2026 Curtis Chou

Description:
  PreToolUse hook（層 0，機器可判定規則）。攔 Bash：指令若是 git commit，
  先掃 staged diff（帶 -a/--all 時加掃工作區 diff）的新增行，命中除錯碼
  pattern 就 block。機器強制 hard-rules.md「Git 紀律：不 commit 除錯碼」
  （2026-07-06 紅隊審查 M4 補入的層 0 規則）。

Features:
  - 只掃「新增行」（diff 的 + 行），刪除除錯碼的 commit 不會被誤擋。
  - pattern 只收無歧義的除錯敘述（各語言常見的主控台印出、中斷點、逐步除錯、
    變數傾印呼叫，見 DEBUG_RE 定義）；不含裸 print 呼叫——Python CLI 的正當
    輸出太多，寧漏勿誤擋。hard-rules 提的 print 該由 code review 把關。
  - 誤判逃生口：指令內含 SKIP_DEBUG_GUARD=1 即放行（會寫 log 留痕，供稽核
    是否被濫用）。
  - fail-open：git 不存在、不在 repo、timeout、任何內部錯誤 → 放行＋log。

Dependencies:
  - Python 3.8+（僅標準函式庫：datetime, json, os, re, subprocess, sys, traceback）
  - git（不存在時 fail-open）

Version History:
  1.0.0 (2026-07-06): 初版（Fable 5 收尾審查修補 M4）。
"""

import datetime
import json
import os
import re
import subprocess
import sys
import traceback

# ==============================
# 常數
# ==============================

LOG_PATH = os.path.expanduser("~/.claude/hooks/hooks.log")

GIT_COMMIT_RE = re.compile(r"\bgit\b[^\n;|&]*?\bcommit\b")
COMMIT_ALL_RE = re.compile(r"\bcommit\b[^\n;|&]*\s(?:-\w*a\w*\b|--all\b)")

DEBUG_RE = re.compile(
    r"(console\.log\s*\(|\bdebugger\b|breakpoint\s*\(\s*\)|"
    r"\bset_trace\s*\(|\bbinding\.pry\b|\bvar_dump\s*\(|\bdd\s*\()"
)

MAX_REPORT = 5


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
            f.write(f"{ts} commit_guard: {line}\n")
    except Exception:
        pass


# ==============================
# Diff 掃描
# ==============================

def scan_diff(diff_text):
    """掃 diff 新增行，回傳命中除錯碼的 (檔案, 行內容) 清單。

    Args:
        diff_text: git diff -U0 的輸出。

    Returns:
        list[tuple(str, str)]：命中清單（最多 MAX_REPORT 筆）。
    """
    hits = []
    current_file = "?"
    for line in diff_text.splitlines():
        if line.startswith("+++ "):
            path = line[4:]
            if path.startswith(("a/", "b/")):
                path = path[2:]
            current_file = path or "?"
            continue
        if not line.startswith("+") or line.startswith("+++"):
            continue
        added = line[1:]
        if DEBUG_RE.search(added):
            hits.append((current_file, added.strip()[:80]))
            if len(hits) >= MAX_REPORT:
                break
    return hits


def collect_diffs(cwd, command):
    """收集要掃的 diff：staged 一定掃；commit -a/--all 加掃工作區。

    Args:
        cwd: 執行目錄。
        command: 原始 Bash 指令（判斷是否帶 -a）。

    Returns:
        str：合併後的 diff 文字。
    """
    texts = []
    cmds = [["git", "-C", cwd, "diff", "--cached", "-U0"]]
    if COMMIT_ALL_RE.search(command):
        cmds.append(["git", "-C", cwd, "diff", "-U0"])
    for c in cmds:
        r = subprocess.run(c, capture_output=True, text=True, timeout=5)
        if r.returncode == 0:
            texts.append(r.stdout)
    return "\n".join(texts)


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

        if not GIT_COMMIT_RE.search(command):
            return 0
        if "SKIP_DEBUG_GUARD=1" in command:
            _log(f"SKIP 逃生口被使用: {command[:120]}")
            return 0

        cwd = data.get("cwd") or os.getcwd()
        hits = scan_diff(collect_diffs(cwd, command))
        if not hits:
            return 0

        listing = "\n".join(f"  {f}: {content}" for f, content in hits)
        _log(f"BLOCK commit 含除錯碼 ({len(hits)}+ 筆): {hits[0][0]}")
        sys.stderr.write(
            "[commit_guard] 依 hard-rules.md「Git 紀律」：不 commit 除錯碼。"
            "staged 變更的新增行命中：\n"
            f"{listing}\n"
            "請移除除錯碼後再 commit。若確認是誤判（例如字串字面值），"
            "先向使用者說明，經同意後在指令前加 SKIP_DEBUG_GUARD=1 重跑"
            "（會留 log 供稽核）。\n"
        )
        return 2
    except Exception:
        # fail-open：hook 本身出任何錯都不可以擋住正常工作；但要留痕。
        _log("ERROR " + traceback.format_exc().replace("\n", " | "))
        return 0


if __name__ == "__main__":
    sys.exit(main())
