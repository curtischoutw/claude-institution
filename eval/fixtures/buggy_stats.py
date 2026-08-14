# eval fixture（t3 除錯任務）— 對一份日誌等級序列（如 ["OK", "ERROR", ...]）
# 計算簡單統計量。供除錯任務使用，行為在某個邊界情況下刻意不正確。
#
# Features:
#   - error_rate：計算 ERROR 佔比
#   - longest_error_streak：計算最長連續 ERROR 長度
#
# Dependencies:
#   - (none, stdlib only)


def error_rate(levels):
    """計算 ERROR 等級在整個序列中的佔比。

    Args:
        levels (list[str]): 日誌等級序列，例如 ["OK", "ERROR", "OK"]。

    Returns:
        float: ERROR 筆數 / 總筆數；序列為空回傳 0.0。
    """
    if not levels:
        return 0.0
    error_count = sum(1 for level in levels if level == "ERROR")
    return error_count / len(levels)


def longest_error_streak(levels):
    """計算最長連續 ERROR 的長度。

    Args:
        levels (list[str]): 日誌等級序列，例如 ["OK", "ERROR", "ERROR", "OK"]。

    Returns:
        int: 最長連續 ERROR 長度；序列為空回傳 0。
    """
    longest = 0
    current = 0
    for i in range(len(levels) - 1):
        if levels[i] == "ERROR":
            current += 1
            longest = max(longest, current)
        else:
            current = 0
    return longest
