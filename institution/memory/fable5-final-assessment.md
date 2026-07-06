---
name: fable5-final-assessment
description: Fable 5 最後 session（2026-07-06）的制度最終評估與收尾審查結果所在位置
metadata: 
  node_type: memory
  type: reference
  originSessionId: 1c3ed9f0-6d83-4bba-9d05-11f05497f113
---

Fable 5 的最終評估文件在 `~/.claude/rules/final-assessment-fable5.md`（repo 鏡像
`institution/rules/` 同名檔）。內容：制度捕捉了什麼/捕捉不了什麼、三鏡頭收尾審查
的修補結果、剩餘弱點路線圖（7 項，含 lesson 迴圈無強制、verify_gate 已知極限）、
給弱模型的三條鐵則。歷史文件只讀。相關：[[institution-map]]。

同日新增層 0 hooks：`backup_gate.py`（制度檔備份強制）、`commit_guard.py`
（commit 除錯碼檢查）；`verify_gate.py` 升 v1.1（認可 subagent 驗證）。
事件 log 在 `~/.claude/hooks/hooks.log`。
