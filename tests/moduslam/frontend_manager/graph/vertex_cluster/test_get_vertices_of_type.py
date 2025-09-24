from moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from moduslam.frontend_manager.main_graph.vertices.custom import (
    LinearVelocity,
    Pose,
)


def test_get_vertices_of_type_empty_cluster():
    cluster = VertexCluster()
    result = cluster.get_vertices_of_type(Pose)
    assert result == ()


def test_get_vertices_of_type_no_matching_type():
    cluster = VertexCluster()
    v1 = Pose(0)
    t1 = 0
    cluster.add(v1, t1)

    result = cluster.get_vertices_of_type(LinearVelocity)
    assert result == ()


def test_get_vertices_of_type_1_vertex():
    cluster = VertexCluster()
    v = Pose(0)
    t = 0
    cluster.add(v, t)

    poses = cluster.get_vertices_of_type(Pose)

    assert len(poses) == 1

    pose = poses[0]
    assert pose in cluster
    assert pose is v


def test_get_vertices_of_type_does_not_modify_original_objects():
    cluster = VertexCluster()
    v1, v2 = Pose(0), Pose(1)
    original_vertices = (v1, v2)

    cluster.add(v1, 0)
    cluster.add(v2, 0)

    vertices = cluster.get_vertices_of_type(Pose)

    assert vertices == original_vertices
