#!/usr/bin/env bash
#
# 把本專案 institution/ 快照中的制度檔還原回 ~/.claude/。
# 遵守制度硬規則 #9：覆寫任何既有檔前，先備份到 ~/.claude/backups/restore-<timestamp>/。
# memory 因路徑含專案名、屬 project-scope，僅印出提示不自動覆寫。
#
# Features:
#   - 還原 CLAUDE.md、rules/、rules-lib/、skills/（動態列舉）、agents/、statusline.sh 到 ~/.claude/
#   - 還原 agents/（對抗審查 subagent）
#   - hooks/ 預設略過，需 --with-hooks 才還原（還原後補 +x）：快照裡的 hooks 是
#     去識別化版本，註解中的路徑範例已改為 <username> 佔位，整包還原會劣化正本
#   - settings.json 預設略過，需 --with-settings 才還原：快照裡 hook 綁定的絕對
#     路徑同樣是 <username> 佔位，還原時用 whoami 替換回實際路徑（sed，非直接 cp）
#   - 覆寫前自動時間戳備份，可回溯
#   - --dry-run 只印動作不實際複製
#
# Dependencies:
#   - bash >= 3.2, coreutils (cp, mkdir, chmod), sed

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
WITH_HOOKS=0
WITH_SETTINGS=0
for arg in "$@"; do
  case "$arg" in
    --dry-run)       DRY_RUN=1 ;;
    --with-hooks)    WITH_HOOKS=1 ;;
    --with-settings) WITH_SETTINGS=1 ;;
    *) echo "未知參數：${arg}（可用：--dry-run、--with-hooks、--with-settings）" >&2; exit 1 ;;
  esac
done

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
# 備份既有檔後複製並替換 <username> 佔位（settings.json 專用）
# ==============================
restore_settings() {
  local rel="settings.json"
  local src="$SRC/$rel"
  local dst="$DEST/$rel"
  [ -f "$src" ] || { echo "略過（快照缺）：$rel"; return; }
  if [ -f "$dst" ]; then
    echo "備份既有：$rel -> backups/restore-$TS/$rel"
    if [ "$DRY_RUN" = 0 ]; then
      mkdir -p "$BACKUP_DIR"
      cp "$dst" "$BACKUP_DIR/$rel"
    fi
  fi
  echo "還原：${rel}（<username> -> $(whoami)）"
  if [ "$DRY_RUN" = 0 ]; then
    sed "s|<username>|$(whoami)|g" "$src" > "$dst"
  fi
}

# ==============================
# 執行還原
# ==============================
restore_file "CLAUDE.md"
restore_file "statusline.sh"
if [ "$DRY_RUN" = 0 ] && [ -f "$DEST/statusline.sh" ]; then
  chmod +x "$DEST/statusline.sh"
fi

for f in "$SRC"/rules/*.md; do
  restore_file "rules/$(basename "$f")"
done

for f in "$SRC"/rules-lib/*.md; do
  restore_file "rules-lib/$(basename "$f")"
done

for f in "$SRC"/skills/*/SKILL.md; do
  restore_file "skills/$(basename "$(dirname "$f")")/SKILL.md"
done

for f in "$SRC"/agents/*.md; do
  restore_file "agents/$(basename "$f")"
done

if [ "$WITH_HOOKS" = 1 ]; then
  for f in "$SRC"/hooks/*; do
    restore_file "hooks/$(basename "$f")"
  done
  if [ "$DRY_RUN" = 0 ]; then
    chmod +x "$DEST"/hooks/* 2>/dev/null || true
  fi
else
  echo "略過 hooks/：快照是去識別化版本（placeholder email/username），覆蓋會劣化正本。"
  echo "  確定要還原 hooks 請加 --with-hooks，並記得事後回填個人化欄位。"
fi

if [ "$WITH_SETTINGS" = 1 ]; then
  restore_settings
else
  echo "略過 settings.json：快照是去識別化版本（hook 路徑 <username> 佔位）。"
  echo "  確定要還原請加 --with-settings（還原時自動替換為 $(whoami)）。"
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
