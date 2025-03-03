import pytest

from src.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from src.moduslam.frontend_manager.main_graph.vertices.custom import Pose
from src.utils.exceptions import ItemExistsError


def test_add():
    cluster = VertexCluster()
    v = Pose(0)
    t = 0
    cluster.add(v, t)

    assert v in cluster
    assert cluster.vertices_with_timestamps == {v: {t: 1}}
    assert cluster.time_range.start == cluster.time_range.stop == t
    assert cluster.empty is False
    assert cluster.vertices == (v,)


def test_add_multiple_vertices():
    cluster = VertexCluster()
    t1, t2 = 1, 2
    v1, v2 = Pose(0), Pose(1)

    cluster.add(v1, t1)
    cluster.add(v2, t2)

    assert v1 in cluster
    assert v2 in cluster
    assert cluster.vertices_with_timestamps == {v1: {t1: 1}, v2: {t2: 1}}
    assert cluster.time_range.start == 1
    assert cluster.time_range.stop == 2
    assert cluster.empty is False
    assert cluster.vertices == (v1, v2)


def test_add_duplicate_vertex_raises_error():
    cluster = VertexCluster()
    v = Pose(0)

    cluster.add(v, 1)

    with pytest.raises(ItemExistsError):
        cluster.add(v, 2)

    assert cluster.empty is False
    assert cluster.vertices == (v,)


def test_time_range_for_multiple_vertices():
    cluster = VertexCluster()
    t1, t2, t3 = 1, 2, 3
    v1, v2, v3 = Pose(0), Pose(1), Pose(2)

    cluster.add(v1, t1)
    cluster.add(v2, t2)
    cluster.add(v3, t3)

    assert cluster.vertices_with_timestamps == {v1: {t1: 1}, v2: {t2: 1}, v3: {t3: 1}}
    assert cluster.empty is False
    assert cluster.time_range.start == 1
    assert cluster.time_range.stop == 3
    assert cluster.vertices == (v1, v2, v3)
