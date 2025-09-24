from typing import Any

import pytest

from moduslam.frontend_manager.main_graph.data_classes import NewVertex
from moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from moduslam.frontend_manager.main_graph.vertex_storage.storage import (
    VertexStorage,
)
from moduslam.frontend_manager.main_graph.vertices.base import (
    NonOptimizableVertex,
    OptimizableVertex,
    Vertex,
)
from moduslam.frontend_manager.main_graph.vertices.custom import Feature3D, Pose
from moduslam.utils.exceptions import ValidationError
from moduslam.utils.ordered_set import OrderedSet


class FakeVertex(Vertex):
    def update(self, value: Any): ...


def test_add_1_vertex():
    storage = VertexStorage()
    cluster = VertexCluster()
    v = Pose(0)
    t = 0
    cluster_set = OrderedSet[VertexCluster]()
    opt_vertices_set = OrderedSet[OptimizableVertex]()
    non_opt_vertices_set = OrderedSet[NonOptimizableVertex]()
    cluster_set.add(cluster)
    opt_vertices_set.add(v)
    new = NewVertex(v, cluster, t)

    storage.add(new)

    assert v in cluster
    assert storage.clusters == cluster_set
    assert storage.vertices == (v,)
    assert storage.optimizable_vertices == opt_vertices_set
    assert storage.non_optimizable_vertices == non_opt_vertices_set


def test_add_non_optimizable_vertex():
    storage = VertexStorage()
    cluster = VertexCluster()
    v = Feature3D(0)
    t = 0
    cluster_set = OrderedSet[VertexCluster]()
    opt_vertices_set = OrderedSet[OptimizableVertex]()
    non_opt_vertices_set = OrderedSet[NonOptimizableVertex]()
    cluster_set.add(cluster)
    non_opt_vertices_set.add(v)
    vertex = NewVertex(v, cluster, t)

    storage.add(vertex)

    assert storage.clusters == cluster_set
    assert storage.vertices == (v,)
    assert storage.optimizable_vertices == opt_vertices_set
    assert storage.non_optimizable_vertices == non_opt_vertices_set
    assert v in storage.non_optimizable_vertices


def test_add_multiple_vertices_of_same_type():
    t = 0
    storage = VertexStorage()
    cluster = VertexCluster()
    v1, v2, v3 = Pose(0), Pose(1), Pose(2)
    cluster_set = OrderedSet[VertexCluster]()
    opt_vertices_set = OrderedSet[OptimizableVertex]()
    non_opt_vertices_set = OrderedSet[NonOptimizableVertex]()
    cluster_set.add(cluster)
    opt_vertices_set.add(v1)
    opt_vertices_set.add(v2)
    opt_vertices_set.add(v3)
    new1 = NewVertex(v1, cluster, t)
    new2 = NewVertex(v2, cluster, t)
    new3 = NewVertex(v3, cluster, t)

    storage.add(new1)
    storage.add(new2)
    storage.add(new3)

    assert v1 in cluster and v2 in cluster and v3 in cluster
    assert storage.clusters == cluster_set
    assert storage.vertices == (v1, v2, v3)
    assert storage.optimizable_vertices == opt_vertices_set
    assert storage.non_optimizable_vertices == non_opt_vertices_set
    assert v1 in storage.optimizable_vertices
    assert v2 in storage.optimizable_vertices
    assert v3 in storage.optimizable_vertices
    assert v1 not in storage.non_optimizable_vertices
    assert v2 not in storage.non_optimizable_vertices
    assert v3 not in storage.non_optimizable_vertices
    assert cluster in storage.clusters


def test_add_same_vertex_twice():
    storage = VertexStorage()
    cluster = VertexCluster()
    v = Pose(0)
    t = 0

    new = NewVertex(v, cluster, t)

    storage.add(new)

    with pytest.raises(ValidationError):
        storage.add(new)


def test_add_vertex_of_incorrect_type():
    storage = VertexStorage()
    cluster = VertexCluster()
    v = FakeVertex(0)
    t = 0

    new = NewVertex(v, cluster, t)

    with pytest.raises(TypeError):
        storage.add(new)


def test_add_updates_indices():
    storage = VertexStorage()
    cluster = VertexCluster()
    v = Pose(0)
    t = 0
    new = NewVertex(v, cluster, t)

    storage.add(new)

    last_pose = storage.get_last_vertex(Pose)

    assert v in storage
    assert last_pose is not None
    assert last_pose.index == 0


def test_add_multiple_clusters_with_equal_timestamp():
    storage = VertexStorage()
    cluster1, cluster2 = VertexCluster(), VertexCluster()
    v1, v2, v3 = Pose(0), Pose(1), Pose(2)
    t = 0

    new1 = NewVertex(v1, cluster1, t)
    new2 = NewVertex(v2, cluster1, t)
    new3 = NewVertex(v3, cluster2, t)

    storage.add(new1)
    storage.add(new2)
    with pytest.raises(ValidationError):
        storage.add(new3)

    assert v1 in storage
    assert v2 in storage
    assert v3 not in storage


def test_no_time_range_intersection():
    storage = VertexStorage()
    cluster1, cluster2 = VertexCluster(), VertexCluster()
    v1, v2 = Pose(0), Pose(1)
    t1, t2 = 0, 1
    new1 = NewVertex(v1, cluster1, t1)
    new2 = NewVertex(v2, cluster2, t2)

    storage.add(new1)
    storage.add(new2)

    with pytest.raises(ValidationError):
        storage.add(NewVertex(v1, cluster2, t1))

    with pytest.raises(ValidationError):
        storage.add(NewVertex(v2, cluster1, t2))

    assert len(storage.clusters) == 2
    assert storage.get_cluster(t1) == cluster1
    assert storage.get_cluster(t2) == cluster2
