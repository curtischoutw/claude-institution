#!/usr/bin/env python3
"""
File: verify_gate.py
Author: Curtis Chou
Email: brokendays611@gmail.com
Created Date: 2026-07-05
Version: 1.0.0
Copyright (c) 2026 Curtis Chou

Description:
  Stop hook（層 0，機器可判定規則）。在每次 session 要結束(Stop 事件)時檢查：
  本回合是否用 Edit/Write/NotebookEdit 動了程式碼副檔名的檔案，卻沒有出現任何
  測試/驗證指令。若是，擋下這次 Stop 並要求走 /done-check。

  設計取材自 Miguok/fable-harness 的 verify_gate.py（同款 Stop-hook + fail-open
  機制），但判斷邏輯保留、訊息全部改寫成指向本專案自己的規則
  （~/.claude/rules/hard-rules.md #5、/done-check skill），不引入 fable 的
  FABLE-PROTOCOL 命名或協定文字，避免與既有制度重複/衝突
  （見 ~/.claude/rules/diagnosis.md 第 2 名：常載膨脹與規則衝突）。

  這是 letter-to-future.md 第 2 點點名的「第一條機器可判定規則」：
  hard-rules.md #5「宣稱完成之前必走 /done-check；回報必附實際指令與輸出」
  原本純靠模型自覺遵守，現在有 hook 機器強制。

Features:
  - 只在偵測到「動了程式碼卻無測試證據」時才擋下；純文件/設定改動不觸發。
  - stop_hook_active（第二次 stop）一律放行，避免純討論 session 被卡死。
  - fail-open：解析 transcript 或任何步驟出錯 → 直接放行，絕不因 hook 本身
    的 bug 卡死使用者的 session。

Dependencies:
  - Python 3.8+（僅標準函式庫：json, re, sys）

Version History:
  1.0.0 (2026-07-05): 初版，改寫自 fable-harness verify_gate.py。
"""

import json
import re
import sys

# ==============================
# 常數：程式碼副檔名、測試指令 pattern、可視為「一次改動」的工具
# ==============================

EDIT_TOOLS = {"Edit", "Write", "NotebookEdit", "MultiEdit"}

CODE_EXTENSIONS = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs",
    ".go", ".rs", ".java", ".rb", ".php", ".c", ".cpp", ".cc", ".h", ".hpp",
    ".cs", ".swift", ".kt", ".kts", ".scala", ".sh", ".bash", ".zsh",
    ".sql", ".lua", ".ex", ".exs", ".clj", ".cljs", ".hs", ".ml", ".mli",
    ".r", ".m", ".mm", ".vue", ".svelte", ".dart", ".jl",
}

TEST_CMD_RE = re.compile(
    r"\b("
    r"pytest|py\.test|python\s+-m\s+pytest|"
    r"npm\s+(?:run\s+)?test|yarn\s+test|pnpm\s+test|"
    r"jest|vitest|"
    r"go\s+test|cargo\s+test|"
    r"mvn\s+test|gradle\s+test|\.\/gradlew\s+test|"
    r"rspec|bundle\s+exec\s+rspec|"
    r"dotnet\s+test|swift\s+test|phpunit|ctest|mix\s+test"
    r")\b",
    re.IGNORECASE,
)

LOCAL_COMMAND_MARKERS = ("<local-command-stdout>", "<command-name>", "<local-command-caveat>")


# ==============================
# Transcript 解析
# ==============================

def load_transcript(path):
    """讀取 transcript JSONL，逐行寬容解析（壞行直接跳過）。

    Args:
        path: transcript 檔案路徑。

    Returns:
        list[dict]：成功解析的條目清單；讀不到檔案回傳空清單。
    """
    entries = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return entries


def is_real_user_prompt(entry):
    """判斷這筆條目是否為「真人打的 user 提示」（排除 local-command 回傳、tool_result）。

    Args:
        entry: transcript 中的一筆條目(dict)。

    Returns:
        bool：是否為真實 user 提示。
    """
    if entry.get("type") != "user":
        return False
    message = entry.get("message") or {}
    content = message.get("content")
    if not isinstance(content, str):
        return False
    if any(marker in content for marker in LOCAL_COMMAND_MARKERS):
        return False
    return True


def find_last_prompt_index(entries):
    """找出最後一則真實 user 提示的 index。

    找不到時（理論上正常對話一定會有；只有人為構造的退化 transcript 才會沒有）
    analyze() 會直接回傳 (False, False)，等同靜默放行——這是 fail-open 精神的
    自然延伸，不是遺漏。

    Args:
        entries: transcript 條目清單。

    Returns:
        int | None：找到的 index；找不到回傳 None。
    """
    last_idx = None
    for i, entry in enumerate(entries):
        if is_real_user_prompt(entry):
            last_idx = i
    return last_idx


def analyze(entries):
    """掃描最後一回合，判斷是否「動了程式碼」與「有無測試指令」。

    Args:
        entries: transcript 條目清單。

    Returns:
        tuple(bool, bool)：(edited_code, test_seen)。
    """
    last_idx = find_last_prompt_index(entries)
    if last_idx is None:
        return False, False

    edited_code = False
    test_seen = False

    for entry in entries[last_idx + 1:]:
        message = entry.get("message") or {}
        content = message.get("content")
        if not isinstance(content, list):
            continue
        for block in content:
            if not isinstance(block, dict) or block.get("type") != "tool_use":
                continue
            name = block.get("name")
            tool_input = block.get("input") or {}

            if name in EDIT_TOOLS:
                file_path = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
                for ext in CODE_EXTENSIONS:
                    if file_path.endswith(ext):
                        edited_code = True
                        break

            if name == "Bash":
                command = tool_input.get("command") or ""
                if TEST_CMD_RE.search(command):
                    test_seen = True

    return edited_code, test_seen


# ==============================
# 主流程
# ==============================

def main():
    """Stop hook 進入點。永遠 exit 0；擋下時把 block JSON 寫到 stdout。

    Args:
        （無；讀 stdin）

    Returns:
        int：永遠回傳 0（fail-open by design；擋下與否由 stdout 內容決定）。
    """
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}

        if data.get("stop_hook_active"):
            return 0

        transcript_path = data.get("transcript_path")
        if not transcript_path:
            return 0

        entries = load_transcript(transcript_path)
        edited_code, test_seen = analyze(entries)

        if edited_code and not test_seen:
            reason = (
                "偵測到本回合用 Edit/Write/NotebookEdit 修改了程式碼檔案，"
                "但這個回合裡沒看到任何測試執行指令（如 pytest/npm test 等；"
                "本 hook 只檢查指令是否出現，不檢查其輸出/是否通過）。\n"
                "依 ~/.claude/rules/hard-rules.md #5：宣稱「完成」之前必走 /done-check，"
                "回報必附實際指令與輸出，不得只寫「測試通過」。\n"
                "請先實際跑相關測試/驗證指令並貼出輸出，或走 /done-check；"
                "若這次改動真的不需要測試（例如純設定調整且已用其他方式驗證），"
                "請在結束前說明理由。"
            )
            print(json.dumps({"decision": "block", "reason": reason}, ensure_ascii=False))
            return 0

        return 0
    except Exception:
        # fail-open：hook 本身出任何錯都不可以卡死使用者的 session。
        return 0


if __name__ == "__main__":
    sys.exit(main())
