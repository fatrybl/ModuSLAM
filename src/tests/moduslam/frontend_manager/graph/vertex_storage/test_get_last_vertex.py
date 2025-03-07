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


def test_get_last_vertex_no_clusters():
    storage = VertexStorage()
    last_vertex = storage.get_last_vertex(Pose)
    assert last_vertex is None


def test_get_last_vertex():
    storage = VertexStorage()
    cluster = VertexCluster()
    v = Pose(0)
    t = 0
    new = NewVertex(v, cluster, t)

    storage.add(new)

    last = storage.get_last_vertex(Pose)

    assert last == v


def test_get_last_vertex_none_of_specified_type():
    storage = VertexStorage()
    cluster = VertexCluster()
    v1, v2 = Pose(0), Pose(1)
    t1, t2 = 0, 1

    new1 = NewVertex(v1, cluster, t1)
    new2 = NewVertex(v2, cluster, t2)

    storage.add(new1)
    storage.add(new2)

    class OtherPose(Pose):
        pass

    last_vertex = storage.get_last_vertex(OtherPose)
    assert last_vertex is None


def test_get_last_vertex_multiple_clusters():
    storage = VertexStorage()
    cluster1, cluster2, cluster3 = VertexCluster(), VertexCluster(), VertexCluster()
    v1, v2, v3, v4 = Pose(0), Pose(1), Pose(2), LinearVelocity(0)
    t1, t2, t3 = 0, 1, 2

    new1 = NewVertex(v1, cluster1, t1)
    new2 = NewVertex(v2, cluster2, t2)
    new3 = NewVertex(v3, cluster3, t3)
    new4 = NewVertex(v4, cluster3, t3)

    storage.add(new1)
    storage.add(new2)
    storage.add(new3)
    storage.add(new4)

    last_pose = storage.get_last_vertex(Pose)
    assert last_pose == v3

    last_velocity = storage.get_last_vertex(LinearVelocity)
    assert last_velocity == v4
