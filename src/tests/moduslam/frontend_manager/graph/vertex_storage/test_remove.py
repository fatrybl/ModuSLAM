import pytest

from src.moduslam.frontend_manager.main_graph.data_classes import NewVertex
from src.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from src.moduslam.frontend_manager.main_graph.vertex_storage.storage import (
    VertexStorage,
)
from src.moduslam.frontend_manager.main_graph.vertices.base import OptimizableVertex
from src.moduslam.frontend_manager.main_graph.vertices.custom import Pose
from src.utils.exceptions import ValidationError
from src.utils.ordered_set import OrderedSet


def test_remove_non_existing_vertex_raises_validation_error():
    storage = VertexStorage()
    v = Pose(0)

    with pytest.raises(ValidationError):
        storage.remove(v)


def test_remove_existing_vertex():
    storage = VertexStorage()
    cluster = VertexCluster()
    v = Pose(0)
    t = 0

    new = NewVertex(v, cluster, t)

    storage.add(new)
    storage.remove(v)

    assert v not in storage
    assert storage.clusters == OrderedSet()
    assert storage.vertices == ()
    assert storage.optimizable_vertices == OrderedSet()
    assert storage.non_optimizable_vertices == OrderedSet()
    assert storage.get_vertices(Pose) == OrderedSet()
    assert storage.get_last_vertex(Pose) is None
    assert storage.get_vertex_cluster(v) is None


def test_remove_correct_timestamp_from_timestamp_cluster_table():
    storage = VertexStorage()
    cluster = VertexCluster()
    v = Pose(0)
    t = 0

    new = NewVertex(v, cluster, t)
    storage.add(new)

    assert t in storage._timestamp_cluster_table

    storage.remove(v)

    assert t not in storage._timestamp_cluster_table


def test_remove_vertex_when_multiple_vertices_of_same_type_exist():
    storage = VertexStorage()
    cluster = VertexCluster()
    v1, v2 = Pose(0), Pose(1)
    t1, t2 = 0, 1
    cluster_set = OrderedSet[VertexCluster]()
    opt_vertices_set = OrderedSet[OptimizableVertex]()
    poses_set = OrderedSet[Pose]()
    cluster_set.add(cluster)
    opt_vertices_set.add(v1)
    opt_vertices_set.add(v2)
    poses_set.add(v2)

    new1 = NewVertex(v1, cluster, t1)
    new2 = NewVertex(v2, cluster, t2)

    storage.add(new1)
    storage.add(new2)

    assert v1 in storage
    assert v2 in storage

    storage.remove(v1)

    assert v1 not in storage
    assert v2 in storage
    assert storage.clusters == cluster_set
    assert storage.vertices == (v2,)
    assert storage.get_last_vertex(Pose) == v2
    assert storage.get_vertices(Pose) == poses_set
    assert storage.get_vertex_cluster(v2) == cluster
    assert storage.get_vertex_cluster(v1) is None


def test_remove_vertex_with_non_matching_timestamp():
    storage = VertexStorage()
    cluster = VertexCluster()
    v1, v2 = Pose(0), Pose(1)
    t1, t2 = 0, 1

    new1 = NewVertex(v1, cluster, t1)
    new2 = NewVertex(v2, cluster, t2)

    storage.add(new1)
    storage.add(new2)

    assert t1 in storage._timestamp_cluster_table
    assert t2 in storage._timestamp_cluster_table

    storage.remove(v1)

    assert t1 not in storage._timestamp_cluster_table
    assert t2 in storage._timestamp_cluster_table
