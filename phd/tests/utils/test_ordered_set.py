"""Tests for the OrderedSet class."""

from typing import Any

import pytest

from phd.utils.ordered_set import OrderedSet


def test_add():
    os = OrderedSet[int]()

    os.add(1)

    assert 1 in os
    assert len(os) == 1


def test_add_multiple():
    os = OrderedSet[int]()

    os.add([1, 2, 3])

    assert 1 in os
    assert 2 in os
    assert 3 in os
    assert len(os) == 3


def test_add_non_hashable_exception():
    os = OrderedSet[Any]()

    with pytest.raises(TypeError):
        os.add([1, 2, [3, 4]])  # [3, 4] is not hashable


def test_remove():
    os = OrderedSet[int]()

    os.add(1)
    os.remove(1)

    assert 1 not in os
    assert len(os) == 0


def test_remove_multiple():
    os = OrderedSet[int]()

    os.add([1, 2, 3])
    os.remove([1, 2])

    assert 1 not in os
    assert 2 not in os
    assert 3 in os
    assert len(os) == 1


def test_remove_exception():
    os = OrderedSet[int]()

    os.add(1)

    with pytest.raises(KeyError):
        os.remove(2)


def test_discard():
    os = OrderedSet[int]()

    os.add(1)
    os.discard(1)

    assert 1 not in os
    assert len(os) == 0

    os.add(1)
    os.discard(2)

    assert 1 in os
    assert len(os) == 1


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


def test_insert_at_beginning_end():
    os = OrderedSet[int]()

    os.add(2)
    os.add(3)
    os.insert(1, 0)

    assert os[0] == 1
    assert os[1] == 2
    assert os[2] == 3

    os.clear()
    assert not os

    os.add(1)
    os.add(2)
    os.insert(3, len(os))

    assert os[0] == 1
    assert os[1] == 2
    assert os[2] == 3


def test_insert_in_middle():
    os = OrderedSet[int]()

    os.add(1)
    os.add(3)
    os.insert(2, 1)

    assert os[0] == 1
    assert os[1] == 2
    assert os[2] == 3
    assert len(os) == 3


def test_insert_duplicate_item():
    os = OrderedSet[int]()

    os.add(1)
    os.add(2)
    os.insert(1, 1)

    assert os[0] == 1
    assert os[1] == 2
    assert len(os) == 2
