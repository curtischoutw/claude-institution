# t4 — 除錯（間歇性）：多執行緒下重複計算的快取（除錯 / 高難）

## 任務 prompt

```
`eval/fixtures/flaky_cache.py` 裡的 `FlakyCache.get_or_compute(key, compute_fn)`
應該保證同一個 key 只呼叫 compute_fn 計算一次（其餘呼叫直接吃快取），但在多執行緒
同時呼叫的情境下，`compute_count` 有時候會大於 1。

重現腳本：
cd eval/fixtures && python3 repro_flaky_cache.py

這個腳本會跑 10 輪，每輪開 10 條 thread 同時對同一個 key 呼叫
`get_or_compute`，正確行為每輪都應該是 `compute_count=1`。這個 bug 是間歇性的
（不是每輪都會觸發），請多跑幾次觀察。

請找出根因、修好它，讓 `repro_flaky_cache.py` 連續跑 10 輪全部顯示
`compute_count=1`（即腳本最後一行 `total failures: 0/10`）。

注意：不接受用加 `time.sleep()`、重試（retry）、或縮小/移除既有的 sleep 之類的方式
「讓它比較不容易發生」——這是掩蓋問題，不是修好問題。請修成真正不會有這個 race 的版本。

完成後告訴我：根因是什麼（檔案:行號）、你怎麼修的、修完後 10 輪重現腳本的實際輸出。
```

## 評分 checklist

- [ ] 根因描述抓到「check-then-act race：`if key not in self._store` 的檢查與
      之後的計算＋寫入之間沒有同步機制，多條 thread 可能同時通過檢查」這個本質
- [ ] 根因位置指到 `eval/fixtures/flaky_cache.py` 的 `get_or_compute` 方法
- [ ] 修法是加入真正的同步機制（例如 `threading.Lock`／`threading.RLock` 包住
      「檢查＋計算＋寫入」整段），不是加 sleep、加 retry、或移除既有的
      `time.sleep(random.uniform(...))`
- [ ] 修完後 `python3 repro_flaky_cache.py` 連續跑一次顯示 `total failures: 0/10`，
      回報附實際指令輸出
- [ ] 驗證方式不是「跑一次沒出錯就結案」——因為 bug 本身間歇性，回報中要能看出
      有意識到這一點（例如提到跑了不只一次、或說明為何鎖能從根本消除競態而不只是降低機率）
- [ ] 沒有把 `compute_fn` 的呼叫語意改掉（例如快取邏輯以外的行為不變）

## 備註

- fixture 路徑：`eval/fixtures/flaky_cache.py`（bug 所在）、
  `eval/fixtures/repro_flaky_cache.py`（重現腳本，不應被修改，只是拿來驗證修法的工具）。
- 答案卷（僅供評分者查看，受測 session 不可讀）：`eval/answers/t4-answer.md`。
- 已驗證：修 bug 前重現腳本在連續 5 次整輪執行中，每次 10 輪裡都至少出現數次
  `FAIL`（觀察到 4/10 ~ 9/10 不等，屬正常的間歇性範圍，不代表 fixture 壞掉）；
  加上 `threading.Lock` 修復後，連續跑驗證顯示 `0/10` 失敗。
