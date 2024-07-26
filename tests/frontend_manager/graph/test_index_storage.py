"""Tests for IndexStorage class."""

import pytest

from moduslam.frontend_manager.graph.index_generator import IndexStorage, generate_index


@pytest.fixture
def index_storage():
    return IndexStorage()


def test_num_indices(index_storage):
    assert index_storage.num_indices == 0
    index_storage.add(1)
    assert index_storage.num_indices == 1


def test_min_idx(index_storage):
    assert index_storage.min_idx == 0
    index_storage.add(1)
    assert index_storage.min_idx == 1


def test_max_idx(index_storage):
    assert index_storage.max_idx == 0
    index_storage.add(1)
    assert index_storage.max_idx == 1


def test_indices(index_storage):
    assert index_storage.indices == set()
    index_storage.add(1)
    assert index_storage.indices == {1}


def test_add(index_storage):
    index_storage.add(1)
    assert index_storage.indices == {1}

    index_storage.add(2)
    assert index_storage.indices == {1, 2}

    with pytest.raises(ValueError):
        index_storage.add(-1)


def test_remove_method(index_storage):
    index_storage.add(5)
    index_storage.add(10)
    index_storage.add(15)

    assert index_storage.indices == {5, 10, 15}
    assert index_storage.min_idx == 5
    assert index_storage.max_idx == 15

    index_storage.remove(10)
    assert index_storage.indices == {5, 15}
    assert index_storage.min_idx == 5
    assert index_storage.max_idx == 15

    index_storage.remove(5)
    assert index_storage.indices == {15}
    assert index_storage.min_idx == 15
    assert index_storage.max_idx == 15

    index_storage.remove(15)
    assert index_storage.indices == set()
    assert index_storage.min_idx == 0
    assert index_storage.max_idx == 0

    with pytest.raises(KeyError):
        index_storage.remove(1)


def test_normalize(index_storage):
    index_storage.add(5)
    index_storage.add(10)
    index_storage.normalize()
    assert index_storage.indices == {0, 5}


def test_update_min_max(index_storage):
    index_storage.add(5)
    index_storage.add(10)
    assert index_storage.min_idx == 5
    assert index_storage.max_idx == 10
    index_storage.remove(5)
    assert index_storage.min_idx == 10
    assert index_storage.max_idx == 10


def test_generate_index(index_storage):
    assert generate_index(index_storage) == 1
    index_storage.add(1)
    assert generate_index(index_storage) == 2
    index_storage.add(2)
    assert generate_index(index_storage) == 3
    index_storage.remove(2)
    assert generate_index(index_storage) == 2
