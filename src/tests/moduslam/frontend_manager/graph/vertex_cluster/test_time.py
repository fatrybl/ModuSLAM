import pytest

from src.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from src.moduslam.frontend_manager.main_graph.vertices.custom import Pose


def test_timestamp_empty_cluster_raises_value_error():
    cluster = VertexCluster()

    with pytest.raises(ValueError):
        _ = cluster.time_range


def test_time_1_vertex():
    cluster = VertexCluster()
    v = Pose(0)
    t = 0
    cluster.add(v, t)

    assert cluster.time_range.start == cluster.time_range.stop == t


def test_time_even_num_vertices():
    cluster = VertexCluster()
    v1, v2 = Pose(0), Pose(1)
    t1, t2 = 0, 1
    cluster.add(v1, t1)
    cluster.add(v2, t2)

    assert cluster.time_range.start == t1
    assert cluster.time_range.stop == t2


def test_time_odd_num_vertices():
    cluster = VertexCluster()
    v1, v2, v3 = Pose(0), Pose(1), Pose(2)
    t1, t2, t3 = 1, 2, 3
    cluster.add(v1, t1)
    cluster.add(v2, t2)
    cluster.add(v3, t3)

    assert cluster.time_range.start == t1
    assert cluster.time_range.stop == t3


def test_time_updates_with_new_vertex():
    cluster = VertexCluster()
    v1, v2, v3 = Pose(0), Pose(1), Pose(2)
    t1, t2, t3 = 1, 3, 5
    cluster.add(v1, t1)
    cluster.add(v2, t2)

    assert cluster.time_range.start == t1
    assert cluster.time_range.stop == t2

    cluster.add(v3, t3)

    assert cluster.time_range.start == t1
    assert cluster.time_range.stop == t3


def test_time_updates_when_vertex_removed():
    cluster = VertexCluster()
    v1, v2, v3 = Pose(0), Pose(1), Pose(2)
    t1, t2, t3 = 1, 3, 5
    cluster.add(v1, t1)
    cluster.add(v2, t2)
    cluster.add(v3, t3)

    assert cluster.time_range.start == t1
    assert cluster.time_range.stop == t3

    cluster.remove(v2)

    assert cluster.time_range.start == t1
    assert cluster.time_range.stop == t3

    cluster.remove(v3)

    assert cluster.time_range.start == t1
    assert cluster.time_range.stop == t1


def test_time_with_duplicate_timestamps():
    cluster = VertexCluster()
    v1, v2, v3, v4 = Pose(0), Pose(1), Pose(2), Pose(3)
    t1, t2, t3, t4 = 1, 2, 2, 4
    cluster.add(v1, t1)
    cluster.add(v2, t2)
    cluster.add(v3, t3)
    cluster.add(v4, t4)

    assert cluster.time_range.start == t1
    assert cluster.time_range.stop == t4

    cluster.remove(v4)

    assert cluster.time_range.start == t1
    assert cluster.time_range.stop == t3
