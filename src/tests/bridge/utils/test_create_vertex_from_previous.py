from src.bridge.edge_factories.factory_protocol import VertexWithStatus
from src.bridge.edge_factories.utils import create_vertex_from_previous
from src.moduslam.frontend_manager.main_graph.data_classes import NewVertex
from src.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from src.moduslam.frontend_manager.main_graph.vertex_storage.storage import (
    VertexStorage,
)
from src.moduslam.frontend_manager.main_graph.vertices.custom import Pose


def test_create_vertex_from_new_with_empty_storage():
    storage = VertexStorage()
    p = Pose(0)
    v = VertexWithStatus(p, VertexCluster(), 1, is_new=True)

    new_v = create_vertex_from_previous(storage, v)

    assert new_v is not p
    assert new_v.index == 1
    assert new_v.value == v.instance.value


def test_create_vertex_from_old():
    t = 0
    p = Pose(0)
    cluster = VertexCluster()
    storage = VertexStorage()
    new = NewVertex(p, cluster, t)
    storage.add(new)
    v = VertexWithStatus(p, cluster, t, is_new=False)

    new_v = create_vertex_from_previous(storage, v)

    assert new_v.index == 1
    assert new_v.value == p.value


def test_create_vertex_from_new_with_not_empty_storage():
    t1, t2 = 0, 1
    p1, p2 = Pose(3), Pose(1)
    cluster = VertexCluster()
    storage = VertexStorage()
    new = NewVertex(p1, cluster, t1)
    storage.add(new)

    v = VertexWithStatus(p2, cluster, t2, is_new=True)

    new_v = create_vertex_from_previous(storage, v)

    assert new_v.index == 2
    assert new_v.value == p2.value
