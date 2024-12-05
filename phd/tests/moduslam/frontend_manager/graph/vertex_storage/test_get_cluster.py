from phd.moduslam.frontend_manager.main_graph.new_element import NewVertex
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.frontend_manager.main_graph.vertex_storage.storage import (
    VertexStorage,
)
from phd.moduslam.frontend_manager.main_graph.vertices.custom import Pose


def test_get_cluster_different_timestamps():
    storage = VertexStorage()
    cluster = VertexCluster()
    v = Pose(0)
    t = 0

    result = storage.get_cluster(0)

    assert result is None

    storage.add(NewVertex(v, cluster, t))

    result = storage.get_cluster(1)

    assert result is None

    result = storage.get_cluster(-1)

    assert result is None

    result = storage.get_cluster(0)

    assert result is cluster


def test_get_cluster_multiple_clusters():
    storage = VertexStorage()
    cluster1, cluster2 = VertexCluster(), VertexCluster()
    v1, v2, v3, v4 = Pose(0), Pose(1), Pose(2), Pose(3)
    t1, t2, t3, t4 = 0, 1, 2, 3

    storage.add(NewVertex(v1, cluster1, t1))
    storage.add(NewVertex(v2, cluster1, t2))
    storage.add(NewVertex(v3, cluster2, t3))
    storage.add(NewVertex(v4, cluster2, t4))

    result = storage.get_cluster(t1)
    assert result == cluster1

    result = storage.get_cluster(t2)
    assert result == cluster1

    result = storage.get_cluster(t3)
    assert result == cluster2

    result = storage.get_cluster(t4)
    assert result == cluster2

    storage.remove(v1)
    storage.remove(v2)

    result = storage.get_cluster(t1)
    assert result is None

    result = storage.get_cluster(t2)
    assert result is None
