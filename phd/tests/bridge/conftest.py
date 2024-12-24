import pytest

from phd.measurement_storage.measurements.pose import Pose as PoseMeasurement
from phd.measurement_storage.storage import MeasurementStorage
from phd.moduslam.frontend_manager.main_graph.edges.noise_models import (
    se3_isotropic_noise_model,
)
from phd.moduslam.frontend_manager.main_graph.edges.pose import Pose as PriorPose
from phd.moduslam.frontend_manager.main_graph.graph import Graph, GraphElement
from phd.moduslam.frontend_manager.main_graph.new_element import NewVertex
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.frontend_manager.main_graph.vertices.custom import Pose
from phd.utils.auxiliary_objects import identity3x3 as i3x3
from phd.utils.auxiliary_objects import identity4x4 as i4x4


@pytest.fixture()
def clean_storage():
    MeasurementStorage.clear()


@pytest.fixture
def empty_graph():
    return Graph()


@pytest.fixture
def graph1():
    graph = Graph()
    t1, idx1 = 0, 0
    v1 = Pose(index=idx1)
    noise = se3_isotropic_noise_model(1)
    m1 = PoseMeasurement(t1, i4x4, i3x3, i3x3)
    edge1 = PriorPose(v1, m1, noise)
    cluster = VertexCluster()
    element1 = GraphElement(edge1, [NewVertex(v1, cluster, t1)])
    graph.add_element(element1)
    return graph


@pytest.fixture
def graph2():
    graph = Graph()
    t1, t2 = 0, 1
    idx1, idx2 = 0, 1
    v1, v2 = Pose(index=idx1), Pose(index=idx2)
    noise = se3_isotropic_noise_model(1)
    m1, m2 = PoseMeasurement(t1, i4x4, i3x3, i3x3), PoseMeasurement(t2, i4x4, i3x3, i3x3)
    edge1, edge2 = PriorPose(v1, m1, noise), PriorPose(v2, m2, noise)
    cluster1, cluster2 = VertexCluster(), VertexCluster()
    element1 = GraphElement(edge1, [NewVertex(v1, cluster1, t1)])
    element2 = GraphElement(edge2, [NewVertex(v2, cluster2, t2)])
    graph.add_elements([element1, element2])
    return graph
