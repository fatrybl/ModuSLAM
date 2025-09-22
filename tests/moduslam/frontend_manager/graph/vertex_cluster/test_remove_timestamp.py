import pytest

from moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from moduslam.frontend_manager.main_graph.vertices.custom import Pose
from moduslam.utils.exceptions import ItemNotExistsError


def test_remove_timestamp_from_empty_cluster():
    cluster = VertexCluster()
    v = Pose(0)

    with pytest.raises(ItemNotExistsError):
        cluster.remove_timestamp(v, 0)


def test_remove_single_timestamp():
    cluster = VertexCluster()
    v = Pose(0)
    t1 = 0

    cluster.add(v, t1)

    cluster.remove_timestamp(v, t1)

    assert cluster.vertices_with_timestamps == {}


def test_remove_nonexistent_timestamp():
    cluster = VertexCluster()
    v = Pose(0)
    t1, t2 = 0, 1

    cluster.add(v, t1)

    with pytest.raises(ValueError):
        cluster.remove_timestamp(v, t2)


def test_remove_timestamp():
    cluster = VertexCluster()
    v = Pose(0)
    t1, t2 = 0, 1

    cluster.add(v, t1)
    cluster.add_timestamp(v, t2)

    assert cluster.vertices_with_timestamps == {v: {t1: 1, t2: 1}}
    assert cluster.time_range.start == t1
    assert cluster.time_range.stop == t2

    cluster.remove_timestamp(v, t2)

    assert cluster.vertices_with_timestamps == {v: {t1: 1}}
    assert cluster.time_range.start == t1
    assert cluster.time_range.stop == t1


def test_remove_timestamp_twice():
    cluster = VertexCluster()
    v = Pose(0)
    t1, t2 = 0, 1

    cluster.add(v, t1)
    cluster.add_timestamp(v, t2)
    cluster.add_timestamp(v, t2)

    assert cluster.vertices_with_timestamps == {v: {t1: 1, t2: 2}}
    assert cluster.time_range.start == t1
    assert cluster.time_range.stop == t2

    cluster.remove_timestamp(v, t2)

    assert cluster.vertices_with_timestamps == {v: {t1: 1, t2: 1}}
    assert cluster.time_range.start == t1
    assert cluster.time_range.stop == t2

    cluster.remove_timestamp(v, t2)

    assert cluster.vertices_with_timestamps == {v: {t1: 1}}
    assert cluster.time_range.start == t1
    assert cluster.time_range.stop == t1


def test_remove_timestamps_for_2_vertices():
    cluster = VertexCluster()
    v1, v2 = Pose(0), Pose(1)
    t1, t2 = 0, 1

    cluster.add(v1, t1)
    cluster.add(v2, t2)
    cluster.add_timestamp(v1, t2)
    cluster.add_timestamp(v2, t1)

    assert cluster.vertices_with_timestamps == {v1: {t1: 1, t2: 1}, v2: {t1: 1, t2: 1}}
    assert cluster.time_range.start == t1
    assert cluster.time_range.stop == t2

    cluster.remove_timestamp(v1, t2)

    assert cluster.vertices_with_timestamps == {v1: {t1: 1}, v2: {t1: 1, t2: 1}}
    assert cluster.time_range.start == t1
    assert cluster.time_range.stop == t2

    cluster.remove_timestamp(v2, t1)

    assert cluster.vertices_with_timestamps == {v1: {t1: 1}, v2: {t2: 1}}
    assert cluster.time_range.start == t1
    assert cluster.time_range.stop == t2


def test_remove_all_timestamps():
    cluster = VertexCluster()
    v = Pose(0)
    t1, t2, t3 = 0, 1, 2

    cluster.add(v, t1)
    cluster.add_timestamp(v, t2)
    cluster.add_timestamp(v, t3)

    assert cluster.vertices_with_timestamps == {v: {t1: 1, t2: 1, t3: 1}}
    assert cluster.time_range.start == t1
    assert cluster.time_range.stop == t3

    cluster.remove_timestamp(v, t1)
    cluster.remove_timestamp(v, t2)
    cluster.remove_timestamp(v, t3)

    assert cluster.vertices_with_timestamps == {}

    with pytest.raises(ValueError):
        _ = cluster.time_range


def test_remove_timestamp_from_multiple_vertices():
    cluster = VertexCluster()
    v1, v2 = Pose(0), Pose(1)
    t1, t2, t3 = 0, 1, 2

    cluster.add(v1, t1)
    cluster.add(v2, t2)
    cluster.add_timestamp(v1, t3)
    cluster.add_timestamp(v2, t3)

    assert cluster.vertices_with_timestamps == {v1: {t1: 1, t3: 1}, v2: {t2: 1, t3: 1}}
    assert cluster.time_range.start == t1
    assert cluster.time_range.stop == t3

    cluster.remove_timestamp(v1, t3)
    cluster.remove_timestamp(v2, t3)

    assert cluster.vertices_with_timestamps == {v1: {t1: 1}, v2: {t2: 1}}
    assert cluster.time_range.start == t1
    assert cluster.time_range.stop == t2
