# File Docstring 模板（按需）

<!-- 按需引用檔。觸發時機：建立任何新的原始碼檔案之前（CLAUDE.md 路由表指到這裡）。
     2026-07-13 自 code-standards.md 降層——依 diagnosis.md 常載兩題測試，
     模板全文只在建檔時需要，不必每輪常載。 -->

每個產出的原始碼檔案開頭必備（markdown 設定檔與 SKILL.md 除外），
依語言換用對應的註解符號：

```
File: <filename>
Author: Curtis Chou
Email: <your-email>
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

- 首次建檔 `Version History` 只需一行初版紀錄；之後每次實質修改在最上面加一行並遞增版本號。
- 版本號只存在檔案內（`Version` + `Version History`），永不放進檔名。
