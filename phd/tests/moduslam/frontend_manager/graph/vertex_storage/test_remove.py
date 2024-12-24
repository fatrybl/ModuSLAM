import pytest

from phd.moduslam.frontend_manager.main_graph.new_element import NewVertex
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.frontend_manager.main_graph.vertex_storage.storage import (
    VertexStorage,
)
from phd.moduslam.frontend_manager.main_graph.vertices.custom import Pose
from phd.utils.exceptions import ValidationError
from phd.utils.ordered_set import OrderedSet


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
    assert len(storage.clusters) == 0
    assert len(storage.vertices) == 0
    assert len(storage.optimizable_vertices) == 0
    assert len(storage.non_optimizable_vertices) == 0
    assert storage.get_last_vertex(Pose) is None
    assert storage.get_vertices(Pose) == OrderedSet()
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

    new1 = NewVertex(v1, cluster, t1)
    new2 = NewVertex(v2, cluster, t2)
    final_set = OrderedSet[Pose]()
    final_set.add(v2)

    storage.add(new1)
    storage.add(new2)

    assert v1 in storage
    assert v2 in storage

    storage.remove(v1)

    assert v1 not in storage
    assert v2 in storage
    assert len(storage.clusters) == 1
    assert len(storage.vertices) == 1
    assert storage.get_last_vertex(Pose) == v2
    assert storage.get_vertices(Pose) == final_set
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
