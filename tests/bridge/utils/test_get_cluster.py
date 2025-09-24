from moduslam.bridge.edge_factories.utils import get_cluster
from moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from moduslam.frontend_manager.main_graph.vertex_storage.storage import (
    VertexStorage,
)
from moduslam.utils.auxiliary_dataclasses import TimeRange


def test_get_cluster():
    cls1, cls2 = VertexCluster(), VertexCluster()
    clusters = {cls1: TimeRange(0, 5), cls2: TimeRange(6, 10)}
    t1, t2, t3 = 3, 7, 12
    storage = VertexStorage()

    result = get_cluster(storage, clusters, t1)

    assert result is cls1

    result = get_cluster(storage, clusters, t2)

    assert result is cls2

    result = get_cluster(storage, clusters, t3)

    assert result is not cls1 and result is not cls2
