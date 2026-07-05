# Code Standards（常載）

## File Docstring（每個產出的原始碼檔案必備；markdown 設定檔與 SKILL.md 除外）

```
File: <filename>
Author: Curtis Chou
Email: brokendays611@gmail.com
Created Date: <YYYY-MM-DD>
Version: <x.x.x>
Copyright (c) <created_year>[-<current_year>] Curtis Chou
(omit the trailing year when both years are the same)

Description:
  <functional description and design decisions>

Features:
  - <feature 1>
  - <feature 2>

Dependencies:
  - <package>==<version>

Version History:
  x.x.x (YYYY-MM-DD): <change description>
```

## In-file Structure

- 功能區塊之間用 `# ==============================` 分隔線 + 標籤。
- 每個 function/method docstring 必含 `Args` 與 `Returns`。
- 版本號只存在檔案內（`Version` + `Version History`），永不放進檔名。

## Core Principles

- **Simplicity First**：每個改動盡可能簡單，影響最少的程式碼。
- **No Laziness**：找根因，不做臨時貼補。
- **Surface Assumptions**：所有假設寫出來，永不沉默猜測。
- **Proactive Warnings**：主動指出風險、邊界情況與副作用，即使沒被問。
