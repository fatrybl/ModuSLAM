from phd.moduslam.frontend_manager.main_graph.new_element import NewVertex
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.frontend_manager.main_graph.vertex_storage.storage import (
    VertexStorage,
)
from phd.moduslam.frontend_manager.main_graph.vertices.custom import Pose


def test_add():
    storage = VertexStorage()
    cluster = VertexCluster()
    v = Pose(0)
    t = 0

    new = NewVertex(v, cluster, t)

    storage.add(new)
    storage.remove(v)

    assert v not in storage
    assert len(storage.clusters) == 0
    assert len(storage.vertices) == 0
    assert len(storage.optimizable_vertices) == 0
    assert len(storage.non_optimizable_vertices) == 0
