#!/usr/bin/env python3
"""
File: verify_gate.py
Author: Curtis Chou
Email: <your-email>
Created Date: 2026-07-05
Version: 1.2.0
Copyright (c) 2026 Curtis Chou

Description:
  Stop hook（層 0，機器可判定規則）。在每次 session 要結束(Stop 事件)時檢查：
  本回合是否用 Edit/Write/NotebookEdit 動了程式碼副檔名的檔案，卻沒有出現任何
  測試/驗證指令。若是，擋下這次 Stop 並要求走 /done-check。

  設計取材自 Miguok/fable-harness 的 verify_gate.py（同款 Stop-hook + fail-open
  機制），但判斷邏輯保留、訊息全部改寫成指向本專案自己的規則
  （~/.claude/rules/hard-rules.md #5、/done-check skill），不引入 fable 的
  FABLE-PROTOCOL 命名或協定文字，避免與既有制度重複/衝突
  （原引用 ~/.claude/rules-lib/diagnosis.md 第 2 名：常載膨脹與規則衝突，
  該檔 2026-08-06 已刪並併入 ~/.claude/rules-lib/maintenance.md）。

  本制度的「第一條機器可判定規則」（層 0）：
  hard-rules.md #5「宣稱完成之前必走 /done-check；回報必附實際指令與輸出」
  原本純靠模型自覺遵守，現在有 hook 機器強制。

Features:
  - 只在偵測到「動了程式碼卻無測試證據」時才擋下；純文件/設定改動不觸發。
  - 派 subagent 驗證（Task/Agent 呼叫且 prompt 含測試/驗證意圖）視同有驗證，
    與 hard-rules #11-12「驗證派 subagent、不自驗」對齊——層 0 不再懲罰合規流程。
  - 測試指令採「指令位置」比對（行首或 ;、&、|、( 之後），`cat pytest.ini`
    這類夾帶不再誤判為有跑測試。
  - stop_hook_active（第二次 stop）一律放行，避免純討論 session 被卡死。
  - fail-open：任何內部錯誤 → 放行，但寫入 hooks.log 留痕；block 事件與二次
    Stop 放行也記 log，供人工稽核「被擋後是否敷衍了事」。
  - 沒有測試套件覆蓋的檔案（例如本檔自己）：`python3 -c ast.parse`／`py_compile`／
    `sh -n`／`bash -n`／`node -c` 這類語法檢查指令也視為驗證證據
    （2026-08-07 補；原本只認測試框架指令）。

已知極限（機制上修不掉；2026-07-06 紅隊審查明文記載，勿誤信層 0 全能）:
  - 只驗「測試指令／驗證 agent 是否出現」，驗不了測試是否通過、驗證是否認真。
  - 雙 Stop 逃逸：被 block 後隨便回一句再停就放行（stop_hook_active 放行是
    防卡死的必要洩壓閥）。log 留痕是唯一補償。
  - 偵測窗口只涵蓋「最後一則真人 prompt 之後」；改碼後若使用者再發話，先前
    的 edit 落在窗外。
  - 帶環境變數前綴的指令（FOO=1 pytest）不會被比對到。

Dependencies:
  - Python 3.8+（僅標準函式庫：datetime, json, os, re, sys, traceback）

Version History:
  1.2.0 (2026-08-07): 補語法檢查類指令為驗證證據（新增 SYNTAX_CHECK_RE）——
    本 session 編輯 hooks/*.py 本身時，用 `python3 -c ast.parse` 驗證卻被誤判
    為「沒有測試證據」，因為原偵測只認測試框架指令，沒有測試套件覆蓋的檔案
    （hook 腳本本身）沒有這類指令可跑（使用者核准）。
  1.1.0 (2026-07-06): Fable 5 收尾審查修補——認可 subagent 驗證（修層 0/層 1
    激勵相反）、測試指令比對綁指令位置（堵 cat pytest.ini 夾帶）、補
    .ipynb/.tf/.pl/.pm/.groovy 副檔名、fail-open 與 block 寫 log 留痕、
    明文記載已知極限。
  1.0.0 (2026-07-05): 初版，改寫自 fable-harness verify_gate.py。
"""

import datetime
import json
import os
import re
import sys
import traceback

# ==============================
# 常數：程式碼副檔名、測試指令 pattern、可視為「一次改動」的工具
# ==============================

EDIT_TOOLS = {"Edit", "Write", "NotebookEdit", "MultiEdit"}

# 派 subagent 的工具名（本 harness 為 Agent；舊版/其他 harness 為 Task）
AGENT_TOOLS = {"Task", "Agent"}

CODE_EXTENSIONS = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs",
    ".go", ".rs", ".java", ".rb", ".php", ".c", ".cpp", ".cc", ".h", ".hpp",
    ".cs", ".swift", ".kt", ".kts", ".scala", ".sh", ".bash", ".zsh",
    ".sql", ".lua", ".ex", ".exs", ".clj", ".cljs", ".hs", ".ml", ".mli",
    ".r", ".m", ".mm", ".vue", ".svelte", ".dart", ".jl",
    ".ipynb", ".tf", ".pl", ".pm", ".groovy",
}

TEST_CMD_RE = re.compile(
    r"(?:^|[\n;&|(]\s*)"  # 指令位置：行首或分隔符之後（堵 cat pytest.ini 之類的夾帶）
    r"(?:(?:time|npx|uv\s+run|poetry\s+run|pdm\s+run)\s+)?"  # 常見執行器前綴
    r"("
    r"pytest|py\.test|python3?\s+-m\s+pytest|"
    r"npm\s+(?:run\s+)?test|yarn\s+test|pnpm\s+test|"
    r"jest|vitest|"
    r"go\s+test|cargo\s+test|"
    r"mvn\s+test|gradle\s+test|\.\/gradlew\s+test|"
    r"rspec|bundle\s+exec\s+rspec|"
    r"dotnet\s+test|swift\s+test|phpunit|ctest|mix\s+test"
    r")\b",
    re.IGNORECASE,
)

# 語法檢查類指令：不是測試框架，但足以驗證程式碼至少能被解析/載入
# （2026-08-07 發現的偵測盲區：沒有測試套件覆蓋的檔案——例如本檔自己——
#   慣用的驗證方式是語法檢查，原本會被誤判為「沒驗證」）。
SYNTAX_CHECK_RE = re.compile(
    r"(?:^|[\n;&|(]\s*)"
    r"("
    r"python3?\s+-c\s+.*ast\.parse|"
    r"python3?\s+-m\s+py_compile|"
    r"(?:sh|bash)\s+-n|"
    r"node\s+(?:-c|--check)"
    r")",
    re.IGNORECASE,
)

# 派 subagent 驗證的意圖判定：Task/Agent 呼叫的 prompt/description 含任一即視同驗證
VERIFY_INTENT_RE = re.compile(
    r"(驗證|實跑|跑.{0,6}測試|read-?back|第二意見|"
    r"verif(?:y|ication)|run\s+(?:the\s+)?tests?)",
    re.IGNORECASE,
)

LOG_PATH = os.path.expanduser("~/.claude/hooks/hooks.log")

LOCAL_COMMAND_MARKERS = ("<local-command-stdout>", "<command-name>", "<local-command-caveat>")


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
            f.write(f"{ts} verify_gate: {line}\n")
    except Exception:
        pass


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
        tuple(bool, bool)：(edited_code, test_seen)；test_seen 含「派出帶
        測試/驗證意圖的 subagent」（與 hard-rules #11-12 對齊）。
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
                if TEST_CMD_RE.search(command) or SYNTAX_CHECK_RE.search(command):
                    test_seen = True

            if name in AGENT_TOOLS:
                prompt_text = " ".join(
                    str(tool_input.get(k) or "") for k in ("prompt", "description")
                )
                if VERIFY_INTENT_RE.search(prompt_text):
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
            _log("PASS stop_hook_active（二次 Stop 放行——洩壓閥，留痕供稽核）")
            return 0

        transcript_path = data.get("transcript_path")
        if not transcript_path:
            return 0

        entries = load_transcript(transcript_path)
        edited_code, test_seen = analyze(entries)

        if edited_code and not test_seen:
            reason = (
                "偵測到本回合用 Edit/Write/NotebookEdit 修改了程式碼檔案，"
                "但這個回合裡沒看到任何測試執行指令（如 pytest/npm test 等），"
                "也沒有派出帶驗證意圖的 subagent"
                "（本 hook 只檢查兩者是否出現，不檢查輸出/是否通過）。\n"
                "依 ~/.claude/rules/hard-rules.md #5：宣稱「完成」之前必走 /done-check，"
                "回報必附實際指令與輸出，不得只寫「測試通過」。\n"
                "請三選一：實際跑相關測試/驗證指令並貼出輸出；"
                "派 fresh-context agent 驗證（見 dispatch.md「驗證」節）；或走 /done-check。"
                "若這次改動真的不需要測試（例如純設定調整且已用其他方式驗證），"
                "請在結束前說明理由。"
            )
            _log("BLOCK edited_code=True 且無測試指令/驗證 agent")
            print(json.dumps({"decision": "block", "reason": reason}, ensure_ascii=False))
            return 0

        return 0
    except Exception:
        # fail-open：hook 本身出任何錯都不可以卡死使用者的 session；但要留痕。
        _log("ERROR " + traceback.format_exc().replace("\n", " | "))
        return 0


if __name__ == "__main__":
    sys.exit(main())
