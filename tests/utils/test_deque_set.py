"""Tests for the DequeSet class."""

from slam.utils.deque_set import DequeSet


def test_add():
    ds = DequeSet[int]()
    ds.add(1)
    assert 1 in ds
    assert len(ds) == 1


def test_remove():
    ds = DequeSet[int]()
    ds.add(1)
    ds.remove(1)
    assert 1 not in ds
    assert len(ds) == 0


def test_remove_first():
    ds = DequeSet[int]()
    ds.add(1)
    ds.add(2)
    ds.remove_first()
    assert 1 not in ds
    assert len(ds) == 1


def test_remove_last():
    ds = DequeSet[int]()
    ds.add(1)
    ds.add(2)
    ds.remove_last()
    assert 2 not in ds
    assert len(ds) == 1


def test_sort():
    ds = DequeSet[int]()
    ds.add(2)
    ds.add(1)
    ds.sort(key=lambda x: x)
    assert ds[0] == 1
    assert ds[1] == 2


def test_is_empty():
    ds = DequeSet[int]()
    assert ds.is_empty() is True
    ds.add(1)
    assert ds.is_empty() is False


def test_clear():
    ds = DequeSet[int]()
    ds.add(1)
    ds.clear()
    assert len(ds) == 0


def test_dequeset_equality():
    ds1 = DequeSet[int]()
    ds2 = DequeSet[int]()
    for i in range(5):
        ds1.add(i)
        ds2.add(i)

    assert ds1 == ds2

    ds3 = DequeSet[int]()
    ds4 = DequeSet[int]()
    for i in range(5, 10):
        ds3.add(i)
        ds4.add(i - 1)

    assert ds3 != ds4
