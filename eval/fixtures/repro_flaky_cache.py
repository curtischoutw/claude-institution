# File: repro_flaky_cache.py
# Author: Curtis Chou
# Email: <your-email>
# Created Date: 2026-07-15
# Version: 1.0.0
# Copyright (c) 2026 Curtis Chou
#
# Description:
#   eval fixture — flaky_cache.py 的重現腳本。開 10 條 thread 同時對同一個
#   key 呼叫 FlakyCache.get_or_compute，正確行為應只計算一次
#   （compute_count == 1）。跑 10 輪，把每輪結果與是否失敗印出來，
#   最後印出總失敗次數。
#
# Features:
#   - 單輪重現：10 threads race 同一個 key
#   - 跑 10 輪回報失敗次數，供判斷「10 次內至少偶發一次錯」
#
# Dependencies:
#   - (none, stdlib only)
#
# Version History:
#   1.0.0 (2026-07-15): 初版建立，供 eval t4 間歇性除錯任務使用。

import threading

from flaky_cache import FlakyCache


def run_once():
    """跑一輪 race：10 threads 同時對同一個 key 呼叫 get_or_compute。

    Args:
        (none)

    Returns:
        int: 該輪的 compute_count（正確應為 1）。
    """
    cache = FlakyCache()
    threads = [
        threading.Thread(target=cache.get_or_compute, args=("k", lambda: 42))
        for _ in range(10)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return cache.compute_count


def main():
    """跑 10 輪重現，印出每輪結果與總失敗次數。

    Args:
        (none)

    Returns:
        None
    """
    failures = 0
    for round_no in range(1, 11):
        count = run_once()
        ok = count == 1
        if not ok:
            failures += 1
        print(f"round {round_no}: compute_count={count} {'OK' if ok else 'FAIL (expected 1)'}")
    print(f"total failures: {failures}/10")


if __name__ == "__main__":
    main()
