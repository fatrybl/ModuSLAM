import pytest

from src.moduslam.frontend_manager.main_graph.data_classes import NewVertex
from src.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from src.moduslam.frontend_manager.main_graph.vertex_storage.storage import (
    VertexStorage,
)
from src.moduslam.frontend_manager.main_graph.vertices.base import Vertex
from src.moduslam.frontend_manager.main_graph.vertices.custom import Pose
from src.utils.exceptions import ItemNotExistsError
from src.utils.ordered_set import OrderedSet


def test_remove_timestamp_from_empty_storage():
    storage = VertexStorage()
    v = Pose(0)
    t = 0

    with pytest.raises(ItemNotExistsError):
        storage.remove_vertex_timestamp(v, t)


def test_remove_timestamp():
    storage = VertexStorage()
    cluster = VertexCluster()
    v = Pose(0)
    t = 0
    new = NewVertex(v, cluster, t)
    storage.add(new)

    storage.remove_vertex_timestamp(v, t)

    assert storage.clusters == OrderedSet()
    assert storage.vertices == ()


def test_remove_1_timestamp():
    storage = VertexStorage()
    cluster = VertexCluster()
    v = Pose(0)
    t = 0
    new = NewVertex(v, cluster, t)
    storage.add(new)
    storage.add_vertex_timestamp(v, t)

    storage.remove_vertex_timestamp(v, t)

    assert len(storage.clusters) == 1

    cls = storage.clusters[0]
    assert cls.vertices_with_timestamps == {v: {t: 1}}


def test_remove_timestamp_for_2_vertices():
    storage = VertexStorage()
    cluster = VertexCluster()
    t = 0
    v1, v2 = Pose(0), Pose(1)
    new1, new2 = NewVertex(v1, cluster, t), NewVertex(v2, cluster, t)
    storage.add(new1)
    storage.add(new2)
    storage.add_vertex_timestamp(v1, t)
    storage.add_vertex_timestamp(v2, t)

    storage.remove_vertex_timestamp(v1, t)
    storage.remove_vertex_timestamp(v2, t)

    assert len(storage.clusters) == 1

    cls = storage.clusters[0]
    assert cls.vertices_with_timestamps == {v1: {t: 1}, v2: {t: 1}}


def test_remove_timestamps_for_2_vertices_same_cluster():
    storage = VertexStorage()
    cluster = VertexCluster()
    v1, v2 = Pose(0), Pose(1)
    t1, t2 = 0, 1
    new1, new2 = NewVertex(v1, cluster, t1), NewVertex(v2, cluster, t2)
    storage.add(new1)
    storage.add(new2)
    storage.add_vertex_timestamp(v1, t2)
    storage.add_vertex_timestamp(v2, t1)

    storage.remove_vertex_timestamp(v1, t2)
    storage.remove_vertex_timestamp(v2, t1)

    assert len(storage.clusters) == 1

    cls = storage.clusters[0]
    assert cls.vertices_with_timestamps == {v1: {t1: 1}, v2: {t2: 1}}


def test_remove_timestamps_for_2_vertices_different_clusters():
    storage = VertexStorage()
    cluster1, cluster2 = VertexCluster(), VertexCluster()
    v1, v2 = Pose(0), Pose(1)
    t1, t2 = 0, 1
    new1, new2 = NewVertex(v1, cluster1, t1), NewVertex(v2, cluster2, t2)
    storage.add(new1)
    storage.add(new2)
    storage.add_vertex_timestamp(v1, t1)
    storage.add_vertex_timestamp(v2, t2)

    storage.remove_vertex_timestamp(v1, t1)
    storage.remove_vertex_timestamp(v2, t2)

    assert len(storage.clusters) == 2

    cls1, cls2 = storage.clusters[0], storage.clusters[1]
    assert cls1.vertices_with_timestamps == {v1: {t1: 1}}
    assert cls2.vertices_with_timestamps == {v2: {t2: 1}}


def test_remove_timestamps():
    storage = VertexStorage()
    empty_set = OrderedSet[Vertex | VertexCluster]()
    cluster1, cluster2 = VertexCluster(), VertexCluster()
    v1, v2 = Pose(0), Pose(1)
    t1, t2 = 0, 1
    new1, new2 = NewVertex(v1, cluster1, t1), NewVertex(v2, cluster2, t2)
    storage.add(new1)
    storage.add(new2)

    storage.remove_vertex_timestamp(v1, t1)
    storage.remove_vertex_timestamp(v2, t2)

    assert storage.vertices == ()
    assert storage.clusters == empty_set
    assert storage.non_optimizable_vertices == empty_set
    assert storage.optimizable_vertices == empty_set


def test_remove_all_timestamps():
    storage = VertexStorage()
    empty_set = OrderedSet[Vertex | VertexCluster]()
    cluster1, cluster2 = VertexCluster(), VertexCluster()
    v1, v2 = Pose(0), Pose(1)
    t1, t2, t3, t4 = 0, 1, 2, 3
    new1, new2 = NewVertex(v1, cluster1, t1), NewVertex(v2, cluster2, t2)
    storage.add(new1)
    storage.add(new2)
    storage.add_vertex_timestamp(v1, t3)
    storage.add_vertex_timestamp(v2, t4)

    storage.remove_vertex_timestamp(v1, t1)
    storage.remove_vertex_timestamp(v1, t3)
    storage.remove_vertex_timestamp(v2, t2)
    storage.remove_vertex_timestamp(v2, t4)

    assert storage.vertices == ()
    assert storage.clusters == empty_set
    assert storage.non_optimizable_vertices == empty_set
    assert storage.optimizable_vertices == empty_set
