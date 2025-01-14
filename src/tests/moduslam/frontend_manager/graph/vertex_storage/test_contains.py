from src.moduslam.frontend_manager.main_graph.data_classes import NewVertex
from src.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from src.moduslam.frontend_manager.main_graph.vertex_storage.storage import (
    VertexStorage,
)
from src.moduslam.frontend_manager.main_graph.vertices.custom import (
    LinearVelocity,
    Pose,
)


def test_contains():
    storage = VertexStorage()
    v = Pose(0)

    assert v not in storage


def test_contains_when_item_is_present():
    storage = VertexStorage()
    cluster = VertexCluster()
    v = Pose(0)
    t = 0
    new = NewVertex(v, cluster, t)
    storage.add(new)

    assert v in storage


def test_contains_with_unknown_type():
    storage = VertexStorage()
    unknown_item = "unknown_type_item"

    assert unknown_item not in storage


def test_contains_multiple_vertices():
    storage = VertexStorage()
    cluster = VertexCluster()
    v1, v2 = Pose(0), LinearVelocity(1)
    t1, t2 = 0, 1

    new1 = NewVertex(v1, cluster, t1)
    new2 = NewVertex(v2, cluster, t2)
    storage.add(new1)
    storage.add(new2)

    assert v1 in storage
    assert v2 in storage


def test_contains_vertex_is_removed():
    storage = VertexStorage()
    cluster = VertexCluster()
    v = Pose(0)
    t = 0
    new = NewVertex(v, cluster, t)

    storage.add(new)
    storage.remove(v)

    assert v not in storage


def test_contains_remove_multiple_vertices():
    storage = VertexStorage()
    cluster = VertexCluster()
    v1, v2 = Pose(0), LinearVelocity(1)
    t1, t2 = 0, 1

    new1 = NewVertex(v1, cluster, t1)
    new2 = NewVertex(v2, cluster, t2)

    storage.add(new1)
    storage.add(new2)

    storage.remove(v1)

    assert v1 not in storage
    assert v2 in storage

    storage.remove(v2)

    assert v1 not in storage
    assert v2 not in storage
