import pytest

from src.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from src.moduslam.frontend_manager.main_graph.vertices.custom import Pose
from src.utils.exceptions import ItemNotExistsError


def test_add_timestamp_to_empty_cluster():
    cluster = VertexCluster()
    v = Pose(0)

    with pytest.raises(ItemNotExistsError):
        cluster.add_timestamp(v, 0)


def test_add_timestamp():
    cluster = VertexCluster()
    v = Pose(0)
    t1, t2 = 0, 1

    cluster.add(v, t1)

    assert v in cluster
    assert cluster.vertices_with_timestamps == {v: {t1: 1}}
    assert cluster.time_range.start == cluster.time_range.stop == t1
    assert cluster.vertices == (v,)

    cluster.add_timestamp(v, t2)

    assert cluster.vertices_with_timestamps == {v: {t1: 1, t2: 1}}
    assert cluster.time_range.start == t1
    assert cluster.time_range.stop == t2


def test_add_timestamp_twice():
    cluster = VertexCluster()
    v = Pose(0)
    t1, t2 = 0, 1

    cluster.add(v, t1)

    cluster.add_timestamp(v, t2)

    assert cluster.vertices_with_timestamps == {v: {t1: 1, t2: 1}}
    assert cluster.time_range.start == t1
    assert cluster.time_range.stop == t2

    cluster.add_timestamp(v, t2)

    assert cluster.vertices_with_timestamps == {v: {t1: 1, t2: 2}}
    assert cluster.time_range.start == t1
    assert cluster.time_range.stop == t2


def test_add_timestamps_twice_for_2_vertices():
    cluster = VertexCluster()
    v1, v2 = Pose(0), Pose(1)
    t1, t2 = 0, 1

    cluster.add(v1, t1)

    cluster.add_timestamp(v1, t2)

    assert cluster.vertices_with_timestamps == {v1: {t1: 1, t2: 1}}
    assert cluster.time_range.start == t1
    assert cluster.time_range.stop == t2

    cluster.add(v2, t2)

    assert cluster.vertices_with_timestamps == {v1: {t1: 1, t2: 1}, v2: {t2: 1}}
    assert cluster.time_range.start == t1
    assert cluster.time_range.stop == t2

    cluster.add_timestamp(v2, t1)

    assert cluster.vertices_with_timestamps == {v1: {t1: 1, t2: 1}, v2: {t1: 1, t2: 1}}
    assert cluster.time_range.start == t1
    assert cluster.time_range.stop == t2
