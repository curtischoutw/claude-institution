# File: refactor_target.py
# Author: Curtis Chou
# Email: <your-email>
# Created Date: 2026-07-15
# Version: 1.0.0
# Copyright (c) 2026 Curtis Chou
#
# Description:
#   eval fixture — 用平行陣列（parallel arrays）管理一份簡易庫存清單的工具函式集合。
#   刻意保留常見壞味道供重構練習使用，行為本身正確（測試已全綠）。
#
# Features:
#   - 新增／移除／查詢／折扣／統計庫存項目
#   - 三個平行陣列（names/prices/quantities）以索引對齊，而非物件化
#
# Dependencies:
#   - (none, stdlib only)
#
# Version History:
#   1.0.0 (2026-07-15): 初版建立，供 eval t2 重構任務使用。


def add_item(names, prices, quantities, name, price, quantity):
    """新增一筆庫存項目（原地修改三個平行陣列）。

    Args:
        names (list[str]): 品名陣列。
        prices (list[float]): 單價陣列，與 names 索引一一對應。
        quantities (list[int]): 數量陣列，與 names 索引一一對應。
        name (str): 新項目品名。
        price (float): 新項目單價。
        quantity (int): 新項目數量。

    Returns:
        None
    """
    names.append(name)
    prices.append(price)
    quantities.append(quantity)


def find_item_index(names, name):
    """找出品名在陣列中的索引。

    Args:
        names (list[str]): 品名陣列。
        name (str): 要尋找的品名。

    Returns:
        int: 索引；找不到回傳 -1。
    """
    for i in range(len(names)):
        if names[i] == name:
            return i
    return -1


def remove_item(names, prices, quantities, name):
    """移除指定品名的項目（原地修改三個平行陣列）。

    Args:
        names (list[str]): 品名陣列。
        prices (list[float]): 單價陣列。
        quantities (list[int]): 數量陣列。
        name (str): 要移除的品名。

    Returns:
        bool: 是否成功移除。
    """
    idx = find_item_index(names, name)
    if idx == -1:
        return False
    del names[idx]
    del prices[idx]
    del quantities[idx]
    return True


def total_value(names, prices, quantities):
    """計算庫存總值（單價 * 數量加總）。

    Args:
        names (list[str]): 品名陣列（僅用來對齊長度）。
        prices (list[float]): 單價陣列。
        quantities (list[int]): 數量陣列。

    Returns:
        float: 總值。
    """
    total = 0.0
    for i in range(len(names)):
        total += prices[i] * quantities[i]
    return total


def apply_discount(names, prices, quantities, name, discount_pct):
    """對指定品名套用折扣（原地修改 prices）。

    Args:
        names (list[str]): 品名陣列。
        prices (list[float]): 單價陣列。
        quantities (list[int]): 數量陣列（未使用，僅維持介面一致）。
        name (str): 要折扣的品名。
        discount_pct (float): 折扣百分比（0-100）。

    Returns:
        bool: 是否成功套用。
    """
    idx = find_item_index(names, name)
    if idx == -1:
        return False
    prices[idx] = prices[idx] * (1 - discount_pct / 100)
    return True


def most_expensive(names, prices, quantities):
    """找出單價最高的品名。

    Args:
        names (list[str]): 品名陣列。
        prices (list[float]): 單價陣列。
        quantities (list[int]): 數量陣列（未使用，僅維持介面一致）。

    Returns:
        str | None: 單價最高的品名；清單為空回傳 None。
    """
    if not names:
        return None
    best_idx = 0
    for i in range(1, len(names)):
        if prices[i] > prices[best_idx]:
            best_idx = i
    return names[best_idx]


def to_report_lines(names, prices, quantities):
    """把庫存轉成報表文字行。

    Args:
        names (list[str]): 品名陣列。
        prices (list[float]): 單價陣列。
        quantities (list[int]): 數量陣列。

    Returns:
        list[str]: 每行格式 "<name>: <qty> x <price> = <subtotal>"。
    """
    lines = []
    for i in range(len(names)):
        subtotal = prices[i] * quantities[i]
        lines.append(f"{names[i]}: {quantities[i]} x {prices[i]} = {subtotal}")
    return lines
