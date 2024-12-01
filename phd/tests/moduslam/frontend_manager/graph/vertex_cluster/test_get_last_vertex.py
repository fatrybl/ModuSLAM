from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.frontend_manager.main_graph.vertices.custom import (
    LinearVelocity,
    Pose,
)


def test_get_last_vertex_returns_none_when_cluster_is_empty():
    cluster = VertexCluster()

    last = cluster.get_last_vertex(Pose)

    assert last is None


def test_get_last_vertex():
    cluster = VertexCluster()
    v = Pose(0)
    t = 0
    cluster.add(v, t)

    last = cluster.get_last_vertex(Pose)

    assert last is v


def test_get_last_vertex_returns_none_for_nonexistent_type():
    cluster = VertexCluster()
    v = Pose(0)
    t = 0
    cluster.add(v, t)

    last = cluster.get_last_vertex(LinearVelocity)

    assert last is None


def test_get_last_vertex_handles_multiple_types():
    cluster = VertexCluster()
    pose1, pose2 = Pose(0), Pose(1)
    vel1, vel2 = LinearVelocity(0), LinearVelocity(1)

    cluster.add(pose1, 0)
    cluster.add(vel1, 1)
    cluster.add(pose2, 2)
    cluster.add(vel2, 3)

    last_pose = cluster.get_last_vertex(Pose)
    last_velocity = cluster.get_last_vertex(LinearVelocity)

    assert last_pose is pose2
    assert last_velocity is vel2


def test_get_last_vertex_with_multiple_same_type():
    cluster = VertexCluster()
    v1, v2, v3 = Pose(0), Pose(1), Pose(2)

    cluster.add(v1, 0)
    cluster.add(v2, 1)
    cluster.add(v3, 2)

    last_pose = cluster.get_last_vertex(Pose)

    assert last_pose is v3


def test_get_last_vertex_updates_with_new_vertex_of_same_type():
    cluster = VertexCluster()
    v1, v2 = Pose(0), Pose(1)

    cluster.add(v1, 0)
    last_pose = cluster.get_last_vertex(Pose)
    assert last_pose is v1

    cluster.add(v2, 1)
    last_pose = cluster.get_last_vertex(Pose)
    assert last_pose is v2


def test_get_last_vertex_maintains_correct_last_after_removal_and_addition():
    cluster = VertexCluster()
    v1, v2, v3 = Pose(0), Pose(1), Pose(2)

    cluster.add(v1, 0)
    cluster.add(v2, 1)

    cluster.remove(v2)
    last_pose = cluster.get_last_vertex(Pose)
    assert last_pose is v1

    cluster.add(v3, 2)
    last_pose = cluster.get_last_vertex(Pose)
    assert last_pose is v3


def test_get_last_vertex_after_removal_of_type():
    cluster = VertexCluster()
    v1, v2 = Pose(0), Pose(1)

    cluster.add(v1, 0)
    cluster.add(v2, 1)

    cluster.remove(v2)
    cluster.remove(v1)

    last_pose = cluster.get_last_vertex(Pose)
    assert last_pose is None
