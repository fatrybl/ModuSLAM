import pytest

from phd.measurements.processed_measurements import Pose as PoseMeasurement
from phd.moduslam.frontend_manager.main_graph.edges.noise_models import (
    se3_isotropic_noise_model,
)
from phd.moduslam.frontend_manager.main_graph.edges.pose import Pose as PriorPose
from phd.moduslam.frontend_manager.main_graph.graph import Graph, GraphElement
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.frontend_manager.main_graph.vertices.custom import Pose
from phd.moduslam.utils.auxiliary_objects import identity3x3, identity4x4


@pytest.fixture
def empty_graph():
    return Graph()


@pytest.fixture
def graph1():
    graph = Graph()
    t1, idx1 = 0, 0
    v1 = Pose(index=idx1)
    noise = se3_isotropic_noise_model(1)
    m1 = PoseMeasurement(t1, identity4x4, identity3x3, identity3x3, [])
    edge1 = PriorPose(v1, m1, noise)
    new_vertices1 = {VertexCluster(): [(v1, t1)]}
    element1 = GraphElement(edge1, new_vertices1)
    graph.add_element(element1)
    return graph


@pytest.fixture
def graph2():
    graph = Graph()
    t1, t2 = 0, 1
    idx1, idx2 = 0, 1
    v1, v2 = Pose(index=idx1), Pose(index=idx2)
    noise = se3_isotropic_noise_model(1)
    m1 = PoseMeasurement(t1, identity4x4, identity3x3, identity3x3, [])
    m2 = PoseMeasurement(t2, identity4x4, identity3x3, identity3x3, [])
    edge1 = PriorPose(v1, m1, noise)
    edge2 = PriorPose(v2, m2, noise)
    new_vertices1 = {VertexCluster(): [(v1, t1)]}
    new_vertices2 = {VertexCluster(): [(v2, t2)]}
    element1 = GraphElement(edge1, new_vertices1)
    element2 = GraphElement(edge2, new_vertices2)
    graph.add_element(element1)
    graph.add_element(element2)
    return graph
