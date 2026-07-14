# File: flaky_cache.py
# Author: Curtis Chou
# Email: <your-email>
# Created Date: 2026-07-15
# Version: 1.0.0
# Copyright (c) 2026 Curtis Chou
#
# Description:
#   eval fixture — 簡易快取模組，供除錯評測任務使用。已知在某些使用場景下
#   行為不符預期（詳見 eval/answers/，僅評分者可讀）。
#
# Features:
#   - get_or_compute(key, compute_fn)：命中回傳快取值，未命中則呼叫 compute_fn
#     計算、記錄一次計算次數並存入快取
#
# Dependencies:
#   - (none, stdlib only)
#
# Version History:
#   1.0.0 (2026-07-15): 初版建立，供 eval t4 間歇性除錯任務使用。

import random
import time


class FlakyCache:
    """先查詢、未命中才計算的簡易快取。"""

    def __init__(self):
        self._store = {}
        self.compute_count = 0

    def get_or_compute(self, key, compute_fn):
        """回傳 key 對應的快取值；未命中則呼叫 compute_fn 計算並存入。

        Args:
            key (str): 快取鍵。
            compute_fn (Callable[[], Any]): 未命中時用來計算值的函式。

        Returns:
            Any: key 對應的值。
        """
        if key not in self._store:
            time.sleep(random.uniform(0, 0.00001))
            value = compute_fn()
            self.compute_count += 1
            self._store[key] = value
        return self._store[key]
