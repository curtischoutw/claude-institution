#!/usr/bin/env bash
#
# File: restore.sh
# Author: Curtis Chou
# Email: your-email@example.com
# Created Date: 2026-07-05
# Version: 1.0.0
# Copyright (c) 2026 Curtis Chou
#
# Description:
#   把本專案 institution/ 快照中的制度檔還原回 ~/.claude/。
#   遵守制度硬規則 #9：覆寫任何既有檔前，先備份到 ~/.claude/backups/restore-<timestamp>/。
#   memory 因路徑含專案名、屬 project-scope，僅印出提示不自動覆寫。
#
# Features:
#   - 還原 CLAUDE.md、rules/、三個 skills/ 到 ~/.claude/
#   - 還原 agents/（對抗審查 subagent）、hooks/（層 0 hook 腳本，還原後補可執行位元）
#   - 覆寫前自動時間戳備份，可回溯
#   - --dry-run 只印動作不實際複製
#
# Dependencies:
#   - bash >= 3.2, coreutils (cp, mkdir, chmod)
#
# Version History:
#   1.0.0 (2026-07-05): 初版
#   1.1.0 (2026-07-05): 新增 agents/ 與 hooks/ 還原（借鑑 fable-harness 補層 0 hooks
#                        與對抗 subagent 後同步）；hooks/* 還原後補 +x。

set -euo pipefail

# ==============================
# 路徑與參數
# ==============================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$SCRIPT_DIR/institution"
DEST="$HOME/.claude"
TS="$(date +%Y%m%d-%H%M%S)"
BACKUP_DIR="$DEST/backups/restore-$TS"

DRY_RUN=0
[ "${1:-}" = "--dry-run" ] && DRY_RUN=1

if [ ! -d "$SRC" ]; then
  echo "錯誤：找不到快照來源 $SRC" >&2
  exit 1
fi

echo "來源：$SRC"
echo "目標：$DEST"
[ "$DRY_RUN" = 1 ] && echo "模式：DRY-RUN（只印動作，不實際複製）"
echo

# ==============================
# 備份既有檔後複製（單檔）
# ==============================
restore_file() {
  local rel="$1"
  local src="$SRC/$rel"
  local dst="$DEST/$rel"
  [ -f "$src" ] || { echo "略過（快照缺）：$rel"; return; }
  if [ -f "$dst" ]; then
    echo "備份既有：$rel -> backups/restore-$TS/$rel"
    if [ "$DRY_RUN" = 0 ]; then
      mkdir -p "$BACKUP_DIR/$(dirname "$rel")"
      cp "$dst" "$BACKUP_DIR/$rel"
    fi
  fi
  echo "還原：$rel"
  if [ "$DRY_RUN" = 0 ]; then
    mkdir -p "$(dirname "$dst")"
    cp "$src" "$dst"
  fi
}

# ==============================
# 執行還原
# ==============================
restore_file "CLAUDE.md"

for f in "$SRC"/rules/*.md; do
  restore_file "rules/$(basename "$f")"
done

for skill in done-check lesson debug-protocol; do
  restore_file "skills/$skill/SKILL.md"
done

for f in "$SRC"/agents/*.md; do
  restore_file "agents/$(basename "$f")"
done

for f in "$SRC"/hooks/*; do
  restore_file "hooks/$(basename "$f")"
done
if [ "$DRY_RUN" = 0 ]; then
  chmod +x "$DEST"/hooks/* 2>/dev/null || true
fi

# ==============================
# memory：project-scope，不自動覆寫
# ==============================
echo
echo "提醒：memory 屬 project-scope，未自動還原。若需要，手動複製："
echo "  cp $SRC/memory/*.md \\"
echo "     \"$DEST/projects/-Users-$(whoami)-GitHub-claude-institution/memory/\""

echo
if [ "$DRY_RUN" = 1 ]; then
  echo "DRY-RUN 完成，未動任何檔案。"
else
  echo "還原完成。被覆寫的舊檔備份在：$BACKUP_DIR"
fi
