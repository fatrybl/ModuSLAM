from src.moduslam.frontend_manager.main_graph.data_classes import NewVertex
from src.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from src.moduslam.frontend_manager.main_graph.vertex_storage.storage import (
    VertexStorage,
)
from src.moduslam.frontend_manager.main_graph.vertices.custom import Feature3D, Pose


def test_get_last_index_no_vertices():
    storage = VertexStorage()
    index = storage.get_last_index(Pose)
    assert index is None


def test_get_last_index_after_all_vertices_removed():
    storage = VertexStorage()
    cluster = VertexCluster()
    v1, v2 = Pose(0), Pose(1)
    t1, t2 = 0, 1

    storage.add(NewVertex(v1, cluster, t1))
    storage.add(NewVertex(v2, cluster, t2))

    storage.remove(v1)
    storage.remove(v2)

    index = storage.get_last_index(Pose)
    assert index is None


def test_get_last_index():
    storage = VertexStorage()
    cluster = VertexCluster()
    v = Pose(0)
    t = 0

    new = NewVertex(v, cluster, t)

    storage.add(new)

    index = storage.get_last_index(Pose)

    assert index == 0


def test_get_last_index_multiple_vertices_same_type():
    storage = VertexStorage()
    cluster = VertexCluster()
    v1, v2, v3 = Pose(0), Pose(1), Pose(2)
    t1, t2, t3 = 0, 1, 2

    storage.add(NewVertex(v1, cluster, t1))
    storage.add(NewVertex(v2, cluster, t2))
    storage.add(NewVertex(v3, cluster, t3))

    index = storage.get_last_index(Pose)

    assert index == 2


def test_get_last_index_after_removal_and_addition_1():
    storage = VertexStorage()
    cluster = VertexCluster()
    v1, v2 = Pose(0), Pose(1)
    t1, t2 = 0, 1

    storage.add(NewVertex(v1, cluster, t1))
    storage.add(NewVertex(v2, cluster, t2))

    storage.remove(v2)

    storage.add(NewVertex(v2, cluster, t2))

    index = storage.get_last_index(Pose)

    assert index == 1


def test_get_last_index_after_removal_and_addition_2():
    storage = VertexStorage()
    cluster = VertexCluster()
    v1, v2 = Pose(0), Pose(1)
    t1, t2 = 0, 1

    storage.add(NewVertex(v1, cluster, t1))
    storage.add(NewVertex(v2, cluster, t2))

    index = storage.get_last_index(Pose)
    assert index == 1

    storage.remove(v2)

    index = storage.get_last_index(Pose)
    assert index == 0

    storage.add(NewVertex(v2, cluster, t2))

    index = storage.get_last_index(Pose)
    assert index == 1

    storage.remove(v1)
    index = storage.get_last_index(Pose)
    assert index == 1


def test_get_last_index_different_vertex_types():
    storage = VertexStorage()
    cluster = VertexCluster()
    pose1, pose2 = Pose(0), Pose(1)
    feature = Feature3D(0)
    t1, t2, t3 = 0, 1, 2

    storage.add(NewVertex(pose1, cluster, t1))
    storage.add(NewVertex(feature, cluster, t2))
    storage.add(NewVertex(pose2, cluster, t3))

    index_pose = storage.get_last_index(Pose)
    index_non_opt = storage.get_last_index(Feature3D)

    assert index_pose == 1
    assert index_non_opt == 0
