"""Tests for the OrderedSet class."""

from slam.utils.ordered_set import OrderedSet


def test_add():
    os = OrderedSet[int]()
    os.add(1)
    assert 1 in os
    assert len(os) == 1


def test_remove():
    os = OrderedSet[int]()
    os.add(1)
    os.remove(1)
    assert 1 not in os
    assert len(os) == 0


def test_first():
    os = OrderedSet[int]()
    os.add(1)
    os.add(2)
    assert os.first == 1


def test_last():
    os = OrderedSet[int]()
    os.add(1)
    os.add(2)
    assert os.last == 2


def test_items():
    os = OrderedSet[int]()
    os.add(1)
    os.add(2)
    assert list(os.items) == [1, 2]


def test_len():
    os = OrderedSet[int]()
    os.add(1)
    assert len(os) == 1


def test_contains():
    os = OrderedSet[int]()
    os.add(1)
    assert 1 in os


def test_get_item():
    os = OrderedSet[int]()
    os.add(1)
    os.add(2)
    assert os[0] == 1
    assert os[1] == 2


def test_ordered_set_equality():
    os1 = OrderedSet[int]()
    os1.add(1)
    os1.add(2)

    os2 = OrderedSet[int]()
    os2.add(1)
    os2.add(2)

    assert os1 == os2

    os2.add(3)
    assert os1 != os2
