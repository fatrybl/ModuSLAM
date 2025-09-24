import pytest

from moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from moduslam.frontend_manager.main_graph.vertices.custom import Pose
from moduslam.utils.exceptions import ItemNotExistsError


def test_remove_single_vertex():
    cluster = VertexCluster()
    v = Pose(0)
    t = 0
    cluster.add(v, t)
    cluster.remove(v)

    assert v not in cluster
    assert cluster.vertices_with_timestamps == {}
    assert not cluster.vertices

    with pytest.raises(ValueError):
        _ = cluster.time_range


def test_remove_multiple_vertices():
    cluster = VertexCluster()
    t1, t2 = 1, 2
    v1, v2 = Pose(0), Pose(1)
    cluster.add(v1, t1)
    cluster.add(v2, t2)

    cluster.remove(v1)

    assert v1 not in cluster
    assert v2 in cluster
    assert cluster.vertices_with_timestamps == {v2: {t2: 1}}
    assert cluster.time_range.start == cluster.time_range.stop == 2


def test_remove_all_vertices():
    cluster = VertexCluster()
    v1, v2 = Pose(0), Pose(1)

    cluster.add(v1, 1)
    cluster.add(v2, 2)

    cluster.remove(v1)
    cluster.remove(v2)

    assert not cluster.vertices
    assert cluster.empty is True
    assert cluster.vertices_with_timestamps == {}

    with pytest.raises(ValueError):
        _ = cluster.time_range


def test_remove_vertex_not_in_cluster():
    cluster = VertexCluster()
    v1, v2 = Pose(0), Pose(1)

    cluster.add(v1, 1)

    with pytest.raises(ItemNotExistsError):
        cluster.remove(v2)

    assert v1 in cluster


def test_remove_all_vertices_except_one():
    cluster = VertexCluster()
    t1, t2, t3 = 1, 2, 3
    v1, v2, v3 = Pose(0), Pose(1), Pose(2)

    cluster.add(v1, t1)
    cluster.add(v2, t2)
    cluster.add(v3, t3)

    cluster.remove(v1)
    cluster.remove(v2)

    assert cluster.empty is False
    assert cluster.time_range.start == cluster.time_range.stop == t3
    assert cluster.vertices_with_timestamps == {v3: {t3: 1}}


def test_remove_vertex_with_same_timestamp():
    cluster = VertexCluster()
    t = 0
    v1, v2 = Pose(0), Pose(1)

    cluster.add(v1, t)
    cluster.add(v2, t)

    assert cluster.vertices_with_timestamps == {v1: {t: 1}, v2: {t: 1}}

    cluster.remove(v2)

    assert cluster.vertices == (v1,)
    assert cluster.empty is False
    assert cluster.vertices_with_timestamps == {v1: {t: 1}}
