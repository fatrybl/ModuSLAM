"""Tests for the DequeSet class."""

import pytest

from src.utils.deque_set import DequeSet


def test_append():
    ds = DequeSet[int]()

    ds.append(1)

    assert 1 in ds
    assert len(ds) == 1


def test_append_multiple():
    ds = DequeSet[int]()

    items = [1, 2, 3, 4, 5]
    ds.append(items)

    for item in items:
        assert item in ds
    assert len(ds) == len(items)


def test_remove():
    ds = DequeSet[int]()

    ds.append(1)
    ds.remove(1)

    assert 1 not in ds
    assert len(ds) == 0


def test_remove_exception():
    ds = DequeSet[int]()

    with pytest.raises(KeyError):
        ds.remove(1)


def test_remove_first():
    ds = DequeSet[int]()

    ds.append(1)
    ds.append(2)
    ds.remove_first()

    assert 1 not in ds
    assert len(ds) == 1


def test_remove_first_exception():
    ds = DequeSet[int]()

    with pytest.raises(IndexError):
        ds.remove_first()


def test_remove_last():
    ds = DequeSet[int]()

    ds.append(1)
    ds.append(2)
    ds.remove_last()

    assert 2 not in ds
    assert len(ds) == 1


def test_remove_last_exception():
    ds = DequeSet[int]()

    with pytest.raises(IndexError):
        ds.remove_last()


def test_sort():
    ds = DequeSet[int]()

    ds.append(2)
    ds.append(1)

    ds.sort(key=lambda x: x)
    assert ds[0] == 1
    assert ds[1] == 2


def test_empty():
    ds = DequeSet[int]()

    assert ds.empty is True

    ds.append(1)

    assert ds.empty is False


def test_clear():
    ds = DequeSet[int]()

    ds.append(1)
    ds.clear()

    assert len(ds) == 0


def test_equality():
    ds1, ds2 = DequeSet[int](), DequeSet[int]()

    for i in range(5):
        ds1.append(i)
        ds2.append(i)

    assert ds1 == ds2

    ds3 = DequeSet[int]()
    ds4 = DequeSet[int]()

    for i in range(5, 10):
        ds3.append(i)
        ds4.append(i - 1)

    assert ds3 != ds4


def test_getitem_with_valid_index():
    ds = DequeSet[int]()

    ds.append(10)
    ds.append(20)
    ds.append(30)

    assert ds[1] == 20
    assert ds[0:3] == [10, 20, 30]


def test_getitem_with_negative_index():
    ds = DequeSet[int]()

    ds.append(10)
    ds.append(20)
    ds.append(30)

    assert ds[-1] == 30
    assert ds[-2] == 20
    assert ds[-3] == 10


def test_getitem_with_valid_slice():
    ds = DequeSet[int]()

    ds.append([1, 2, 3])

    result = ds[0:3]
    assert result == [1, 2, 3]


def test_getitem_with_out_of_bounds_slice():
    ds = DequeSet[int]()

    ds.append([1, 2, 3])

    result = ds[5:10]
    assert result == []


def test_getitem_with_out_of_bounds_index():
    ds = DequeSet[int]()

    ds.append([1, 2, 3])

    with pytest.raises(IndexError):
        _ = ds[5]


def test_getitem_with_start_greater_than_end_slice():
    ds = DequeSet[int]()

    ds.append([1, 2, 3, 4, 5])

    result = ds[3:1]
    assert result == []


def test_getitem_with_negative_step_slice():
    ds = DequeSet[int]()

    ds.append([1, 2, 3, 4, 5])

    result = ds[4:1:-1]
    assert result == [5, 4, 3]
