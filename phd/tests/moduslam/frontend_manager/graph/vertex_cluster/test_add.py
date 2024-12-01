import pytest

from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.frontend_manager.main_graph.vertices.custom import Pose
from phd.moduslam.utils.exceptions import ItemExistsError


def test_add():
    cluster = VertexCluster()
    v = Pose(0)
    t = 0
    cluster.add(v, t)

    assert v in cluster
    assert cluster.vertices_with_timestamps == {v: t}
    assert cluster.timestamp == t
    assert cluster.time_range.start == cluster.time_range.start == t


def test_add_multiple_vertices():
    cluster = VertexCluster()
    v1 = Pose(0)
    v2 = Pose(1)

    cluster.add(v1, 1)
    cluster.add(v2, 2)

    assert v1 in cluster
    assert v2 in cluster
    assert cluster.vertices_with_timestamps == {v1: 1, v2: 2}
    assert cluster.timestamp == 2
    assert cluster.time_range.start == 1
    assert cluster.time_range.stop == 2


def test_add_duplicate_vertex_raises_error():
    cluster = VertexCluster()
    v = Pose(0)

    cluster.add(v, 1)

    with pytest.raises(ItemExistsError):
        cluster.add(v, 2)


def test_time_range_for_multiple_vertices():
    cluster = VertexCluster()
    v1, v2, v3 = Pose(0), Pose(1), Pose(2)

    cluster.add(v1, 1)
    cluster.add(v2, 2)
    cluster.add(v3, 3)

    assert cluster.time_range.start == 1
    assert cluster.time_range.stop == 3
    assert cluster.timestamp == 2
