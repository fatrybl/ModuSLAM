from typing import Any

import pytest

from phd.moduslam.frontend_manager.main_graph.new_element import NewVertex
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.frontend_manager.main_graph.vertex_storage.storage import (
    VertexStorage,
)
from phd.moduslam.frontend_manager.main_graph.vertices.base import Vertex
from phd.moduslam.frontend_manager.main_graph.vertices.custom import Feature3D, Pose
from phd.utils.exceptions import ValidationError


class FakeVertex(Vertex):
    def update(self, value: Any): ...


def test_add():
    storage = VertexStorage()
    cluster = VertexCluster()
    v = Pose(0)
    t = 0

    new = NewVertex(v, cluster, t)
    storage.add(new)

    assert v in cluster
    assert len(storage.clusters) == 1
    assert len(storage.vertices) == 1
    assert len(storage.optimizable_vertices) == 1
    assert len(storage.non_optimizable_vertices) == 0


def test_add_non_optimizable_vertex():
    storage = VertexStorage()
    cluster = VertexCluster()
    v = Feature3D(0)
    t = 0

    vertex = NewVertex(v, cluster, t)
    storage.add(vertex)

    assert len(storage.clusters) == 1
    assert len(storage.vertices) == 1
    assert len(storage.optimizable_vertices) == 0
    assert len(storage.non_optimizable_vertices) == 1
    assert v in storage.non_optimizable_vertices


def test_add_multiple_vertices_of_same_type():
    t = 0
    storage = VertexStorage()
    cluster = VertexCluster()
    v1, v2, v3 = Pose(0), Pose(1), Pose(2)

    new1 = NewVertex(v1, cluster, t)
    new2 = NewVertex(v2, cluster, t)
    new3 = NewVertex(v3, cluster, t)

    storage.add(new1)
    storage.add(new2)
    storage.add(new3)

    assert v1 in cluster
    assert v2 in cluster
    assert v3 in cluster
    assert len(storage.clusters) == 1
    assert len(storage.vertices) == 3
    assert len(storage.optimizable_vertices) == 3
    assert len(storage.non_optimizable_vertices) == 0
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
