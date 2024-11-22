import pytest

from moduslam.frontend_manager.noise_models import pose_diagonal_noise_model
from phd.bridge.edge_factories.pose_odometry import Factory
from phd.measurements.processed_measurements import Pose as PoseMeasurement
from phd.measurements.processed_measurements import PoseOdometry
from phd.moduslam.frontend_manager.main_graph.edges.pose import Pose as PriorPose
from phd.moduslam.frontend_manager.main_graph.graph import Graph, GraphElement
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.frontend_manager.main_graph.vertices.custom import (
    Pose,
    identity3x3,
    identity4x4,
)
from phd.moduslam.utils.auxiliary_dataclasses import TimeRange


@pytest.fixture
def graph1():
    graph = Graph()
    t1, t2 = 0, 1
    idx1, idx2 = 0, 1
    v1, v2 = Pose(index=idx1), Pose(index=idx2)
    noise = pose_diagonal_noise_model((1, 1, 1, 1, 1, 1))
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


@pytest.fixture
def graph2():
    graph = Graph()
    t1 = 0
    idx1 = 0
    v1 = Pose(index=idx1)
    noise = pose_diagonal_noise_model((1, 1, 1, 1, 1, 1))
    m1 = PoseMeasurement(t1, identity4x4, identity3x3, identity3x3, [])
    edge1 = PriorPose(v1, m1, noise)
    new_vertices1 = {VertexCluster(): [(v1, t1)]}
    element1 = GraphElement(edge1, new_vertices1)
    graph.add_element(element1)
    return graph


def test_create_graph_element_with_0_new_vertices_for_2_existing(graph1):
    measurement = PoseOdometry(1, TimeRange(0, 1), identity4x4, identity3x3, identity3x3, [])
    clusters: dict[VertexCluster, TimeRange] = {VertexCluster(): TimeRange(1, 1)}

    new_element = Factory.create(graph1, clusters, measurement)
    graph1.add_element(new_element)

    assert len(graph1.vertex_storage.vertices) == 2
    assert len(graph1.edge_storage.edges) == 3
    assert len(graph1.vertex_storage.clusters) == 2
    assert len(graph1.connections) == 2
    for edges in graph1.connections.values():
        assert len(edges) == 2


def test_create_graph_element_with_0_new_vertices_for_1_existing(graph2):
    measurement = PoseOdometry(1, TimeRange(0, 1), identity4x4, identity3x3, identity3x3, [])
    clusters: dict[VertexCluster, TimeRange] = {VertexCluster(): TimeRange(1, 1)}

    new_element = Factory.create(graph2, clusters, measurement)
    graph2.add_element(new_element)

    assert len(graph2.vertex_storage.vertices) == 2
    assert len(graph2.edge_storage.edges) == 2
    assert len(graph2.vertex_storage.clusters) == 2
    assert len(graph2.connections) == 2


def test_create_2_graph_elements_with_0_new_for_2_existing(graph1):
    measurement1 = PoseOdometry(1, TimeRange(0, 1), identity4x4, identity3x3, identity3x3, [])
    measurement2 = PoseOdometry(1, TimeRange(0, 1), identity4x4, identity3x3, identity3x3, [])
    clusters: dict[VertexCluster, TimeRange] = {VertexCluster(): TimeRange(1, 1)}

    new_element1 = Factory.create(graph1, clusters, measurement1)
    graph1.add_element(new_element1)
    new_element2 = Factory.create(graph1, clusters, measurement2)
    graph1.add_element(new_element2)

    assert len(graph1.vertex_storage.vertices) == 2
    assert len(graph1.edge_storage.edges) == 4
    assert len(graph1.vertex_storage.clusters) == 2
    assert len(graph1.connections) == 2


def test_create_2_graph_elements_with_1_new_for_1_existing(graph2):
    measurement1 = PoseOdometry(1, TimeRange(0, 1), identity4x4, identity3x3, identity3x3, [])
    measurement2 = PoseOdometry(2, TimeRange(0, 2), identity4x4, identity3x3, identity3x3, [])
    clusters: dict[VertexCluster, TimeRange] = {VertexCluster(): TimeRange(1, 2)}

    new_element1 = Factory.create(graph2, clusters, measurement1)
    graph2.add_element(new_element1)
    new_element2 = Factory.create(graph2, clusters, measurement2)
    graph2.add_element(new_element2)

    assert len(graph2.vertex_storage.vertices) == 2
    assert len(graph2.edge_storage.edges) == 3
    assert len(graph2.vertex_storage.clusters) == 2
    assert len(graph2.connections) == 2


def test_create_graph_element_with_1_new_vertex_for_2_existing(graph1):
    measurement = PoseOdometry(2, TimeRange(0, 2), identity4x4, identity3x3, identity3x3, [])
    clusters: dict[VertexCluster, TimeRange] = {VertexCluster(): TimeRange(2, 2)}

    new_element = Factory.create(graph1, clusters, measurement)
    graph1.add_element(new_element)

    assert len(graph1.vertex_storage.vertices) == 3
    assert len(graph1.edge_storage.edges) == 3
    assert len(graph1.vertex_storage.clusters) == 3
    assert len(graph1.connections) == 3


def test_create_graph_element_with_1_new_vertex_for_1_existing(graph2):
    measurement = PoseOdometry(1, TimeRange(0, 1), identity4x4, identity3x3, identity3x3, [])
    clusters: dict[VertexCluster, TimeRange] = {VertexCluster(): TimeRange(1, 1)}

    new_element = Factory.create(graph2, clusters, measurement)
    graph2.add_element(new_element)

    assert len(graph2.vertex_storage.vertices) == 2
    assert len(graph2.edge_storage.edges) == 2
    assert len(graph2.vertex_storage.clusters) == 2
    assert len(graph2.connections) == 2


def test_create_2_graph_elements_with_1_new_vertex_for_2_existing(graph1):
    measurement1 = PoseOdometry(2, TimeRange(0, 2), identity4x4, identity3x3, identity3x3, [])
    measurement2 = PoseOdometry(3, TimeRange(1, 3), identity4x4, identity3x3, identity3x3, [])
    clusters: dict[VertexCluster, TimeRange] = {VertexCluster(): TimeRange(2, 3)}

    new_element = Factory.create(graph1, clusters, measurement1)
    graph1.add_element(new_element)
    new_element = Factory.create(graph1, clusters, measurement2)
    graph1.add_element(new_element)

    assert len(graph1.vertex_storage.vertices) == 3
    assert len(graph1.edge_storage.edges) == 4
    assert len(graph1.vertex_storage.clusters) == 3
    assert len(graph1.connections) == 3


def test_create_2_graph_elements_with_1_new_vertex_for_1_existing(graph2):
    measurement1 = PoseOdometry(1, TimeRange(0, 1), identity4x4, identity3x3, identity3x3, [])
    measurement2 = PoseOdometry(2, TimeRange(0, 2), identity4x4, identity3x3, identity3x3, [])
    clusters: dict[VertexCluster, TimeRange] = {VertexCluster(): TimeRange(1, 2)}

    new_element = Factory.create(graph2, clusters, measurement1)
    graph2.add_element(new_element)
    new_element = Factory.create(graph2, clusters, measurement2)
    graph2.add_element(new_element)

    assert len(graph2.vertex_storage.vertices) == 2
    assert len(graph2.edge_storage.edges) == 3
    assert len(graph2.vertex_storage.clusters) == 2
    assert len(graph2.connections) == 2


def test_create_2_graph_elements_with_2_new_vertices_for_2_existing(graph1):
    measurement1 = PoseOdometry(2, TimeRange(0, 2), identity4x4, identity3x3, identity3x3, [])
    measurement2 = PoseOdometry(3, TimeRange(1, 3), identity4x4, identity3x3, identity3x3, [])
    clusters: dict[VertexCluster, TimeRange] = {
        VertexCluster(): TimeRange(2, 2),
        VertexCluster(): TimeRange(3, 3),
    }

    new_element = Factory.create(graph1, clusters, measurement1)
    graph1.add_element(new_element)
    new_element = Factory.create(graph1, clusters, measurement2)
    graph1.add_element(new_element)

    assert len(graph1.vertex_storage.vertices) == 4
    assert len(graph1.edge_storage.edges) == 4
    assert len(graph1.vertex_storage.clusters) == 4
    assert len(graph1.connections) == 4


def test_create_2_graph_elements_with_2_new_vertices_for_1_existing(graph2):
    measurement1 = PoseOdometry(1, TimeRange(0, 1), identity4x4, identity3x3, identity3x3, [])
    measurement2 = PoseOdometry(2, TimeRange(1, 2), identity4x4, identity3x3, identity3x3, [])
    clusters: dict[VertexCluster, TimeRange] = {
        VertexCluster(): TimeRange(1, 1),
        VertexCluster(): TimeRange(2, 2),
    }

    new_element = Factory.create(graph2, clusters, measurement1)
    graph2.add_element(new_element)
    new_element = Factory.create(graph2, clusters, measurement2)
    graph2.add_element(new_element)

    assert len(graph2.vertex_storage.vertices) == 3
    assert len(graph2.edge_storage.edges) == 3
    assert len(graph2.vertex_storage.clusters) == 3
    assert len(graph2.connections) == 3
