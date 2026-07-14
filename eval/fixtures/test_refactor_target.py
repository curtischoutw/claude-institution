# File: test_refactor_target.py
# Author: Curtis Chou
# Email: <your-email>
# Created Date: 2026-07-15
# Version: 1.0.0
# Copyright (c) 2026 Curtis Chou
#
# Description:
#   eval fixture — refactor_target.py 的行為基線測試。t2 重構任務要求這份測試
#   在重構前後皆全綠，且測試檔本身不得被修改。
#
# Features:
#   - 涵蓋 add/find/remove/total/discount/most_expensive/report 全部公開函式
#
# Dependencies:
#   - pytest
#
# Version History:
#   1.0.0 (2026-07-15): 初版建立，供 eval t2 重構任務使用。

from refactor_target import (
    add_item,
    apply_discount,
    find_item_index,
    most_expensive,
    remove_item,
    to_report_lines,
    total_value,
)


def _sample():
    names = ["apple", "banana"]
    prices = [1.0, 0.5]
    quantities = [10, 20]
    return names, prices, quantities


def test_add_item_appends_to_all_three_arrays():
    names, prices, quantities = _sample()
    add_item(names, prices, quantities, "cherry", 3.0, 5)
    assert names[-1] == "cherry"
    assert prices[-1] == 3.0
    assert quantities[-1] == 5


def test_find_item_index_found():
    names, prices, quantities = _sample()
    assert find_item_index(names, "banana") == 1


def test_find_item_index_not_found():
    names, prices, quantities = _sample()
    assert find_item_index(names, "durian") == -1


def test_remove_item_success():
    names, prices, quantities = _sample()
    ok = remove_item(names, prices, quantities, "apple")
    assert ok is True
    assert names == ["banana"]
    assert prices == [0.5]
    assert quantities == [20]


def test_remove_item_not_found_returns_false():
    names, prices, quantities = _sample()
    ok = remove_item(names, prices, quantities, "durian")
    assert ok is False
    assert names == ["apple", "banana"]


def test_total_value():
    names, prices, quantities = _sample()
    assert total_value(names, prices, quantities) == 1.0 * 10 + 0.5 * 20


def test_apply_discount_success():
    names, prices, quantities = _sample()
    ok = apply_discount(names, prices, quantities, "apple", 50)
    assert ok is True
    assert prices[0] == 0.5


def test_apply_discount_not_found_returns_false():
    names, prices, quantities = _sample()
    ok = apply_discount(names, prices, quantities, "durian", 50)
    assert ok is False


def test_most_expensive():
    names, prices, quantities = _sample()
    add_item(names, prices, quantities, "cherry", 3.0, 5)
    assert most_expensive(names, prices, quantities) == "cherry"


def test_most_expensive_empty_returns_none():
    assert most_expensive([], [], []) is None


def test_to_report_lines():
    names, prices, quantities = _sample()
    lines = to_report_lines(names, prices, quantities)
    assert lines == ["apple: 10 x 1.0 = 10.0", "banana: 20 x 0.5 = 10.0"]
