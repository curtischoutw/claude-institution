#!/usr/bin/env python3
"""
PreToolUse hook（層 0，機器可判定規則）。攔 Edit/Write/NotebookEdit：
目標若是 ~/.claude/ 下的制度檔（CLAUDE.md、settings.json、rules/、skills/、
hooks/、agents/ 頂層 .md），檢查 ~/.claude/backups/ 是否已有「同檔名＋今日
日期」的備份；沒有就 block 並附上可直接複製的 cp 指令。

機器強制 hard-rules.md #9 的備份要求（2026-07-06 紅隊審查 M3：備份流程
原本純靠模型自覺，弱模型最可能靜默跳過的一步）。

Features:
  - 只攔「既有檔案」的修改；建立新檔不需備份，直接放行。
  - backups/、memory/、plans/、todos/、projects/ 等非制度路徑不攔。
  - agents/ 只保護頂層 .md（自訂 agent 定義），不攔外部 plugin 目錄。
  - block 用 exit 2 + stderr（PreToolUse 標準阻擋方式）。
  - fail-open：任何內部錯誤 → exit 0 放行，寫 hooks.log 留痕。
  - 注意：本 hook 擋不下 Bash 直改（sed -i 等）；那條路徑靠 hard-rules #9
    的模型自覺，屬已知極限。

Dependencies:
  - Python 3.8+（僅標準函式庫：datetime, json, os, sys, traceback）
"""

import datetime
import json
import os
import sys
import traceback

# ==============================
# 常數
# ==============================

CLAUDE_DIR = os.path.expanduser("~/.claude")
BACKUP_DIR = os.path.join(CLAUDE_DIR, "backups")
PROTECTED_SUBDIRS = ("rules", "skills", "hooks")
PROTECTED_TOP_FILES = ("CLAUDE.md", "settings.json")
LOG_PATH = os.path.join(CLAUDE_DIR, "hooks", "hooks.log")


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
            f.write(f"{ts} backup_gate: {line}\n")
    except Exception:
        pass


# ==============================
# 判定邏輯
# ==============================

def is_protected(path):
    """判斷路徑是否為受保護的制度檔。

    Args:
        path: Edit/Write 目標路徑（可含 ~）。

    Returns:
        bool：是否受保護。
    """
    ap = os.path.abspath(os.path.expanduser(path))
    if not ap.startswith(CLAUDE_DIR + os.sep):
        return False
    rel = os.path.relpath(ap, CLAUDE_DIR)
    parts = rel.split(os.sep)
    if len(parts) == 1:
        return parts[0] in PROTECTED_TOP_FILES
    if parts[0] in PROTECTED_SUBDIRS:
        return True
    # agents/ 只保護頂層自訂 agent 定義檔，不攔其下的外部 plugin 目錄
    if parts[0] == "agents" and len(parts) == 2 and parts[1].endswith(".md"):
        return True
    return False


def has_today_backup(path):
    """檢查 backups/ 是否已有該檔今日的備份。

    Args:
        path: 受保護檔案的絕對路徑。

    Returns:
        bool：今日備份是否存在。
    """
    today = datetime.date.today().strftime("%Y%m%d")
    base = os.path.basename(path)
    if not os.path.isdir(BACKUP_DIR):
        return False
    for name in os.listdir(BACKUP_DIR):
        if name.startswith(base + ".") and today in name:
            return True
    return False


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
        path = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
        if not path:
            return 0

        ap = os.path.abspath(os.path.expanduser(path))
        if not is_protected(ap):
            return 0
        if not os.path.exists(ap):
            return 0  # 建立新檔不需備份
        if has_today_backup(ap):
            return 0

        today = datetime.date.today().strftime("%Y%m%d")
        base = os.path.basename(ap)
        _log(f"BLOCK 無今日備份即修改制度檔: {ap}")
        sys.stderr.write(
            f"[backup_gate] 依 hard-rules #9：修改制度檔前先備份。請先執行：\n"
            f'cp "{ap}" "{BACKUP_DIR}/{base}.{today}.bak"\n'
            f"再重試這次修改。另注意：若此檔屬「動前先問」級，"
            f"還需使用者核准——分級見 ~/.claude/rules-lib/maintenance.md。\n"
        )
        return 2
    except Exception:
        # fail-open：hook 本身出任何錯都不可以卡死使用者的 session；但要留痕。
        _log("ERROR " + traceback.format_exc().replace("\n", " | "))
        return 0


if __name__ == "__main__":
    sys.exit(main())
