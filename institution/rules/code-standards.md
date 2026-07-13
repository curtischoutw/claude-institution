# Code Standards（常載）

## File Docstring

每個產出的原始碼檔案必備標準檔頭（markdown 設定檔與 SKILL.md 除外）。
**建立新原始碼檔前，讀 `~/.claude/rules/code-header.md` 取完整模板**——不憑記憶寫。

## In-file Structure

- 功能區塊之間用 `# ==============================` 分隔線 + 標籤。
- 每個 function/method docstring 必含 `Args` 與 `Returns`。
- 版本號只存在檔案內（`Version` + `Version History`），永不放進檔名。

## Core Principles

- **Simplicity First**：每個改動盡可能簡單，影響最少的程式碼。
- **No Laziness**：找根因，不做臨時貼補。
- **Surface Assumptions**：所有假設寫出來，永不沉默猜測。
- **Proactive Warnings**：主動指出風險、邊界情況與副作用，即使沒被問。
