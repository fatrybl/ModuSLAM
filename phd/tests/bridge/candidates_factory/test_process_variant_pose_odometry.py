from phd.bridge.edge_factories.pose_odometry import Factory
from phd.measurements.processed import PoseOdometry
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.utils.auxiliary_dataclasses import TimeRange
from phd.moduslam.utils.auxiliary_objects import identity3x3, identity4x4


def test_create_graph_element_with_0_new_vertices_for_2_existing(graph2):
    t = 1
    measurement = PoseOdometry(t, TimeRange(0, t), identity4x4, identity3x3, identity3x3, [])
    clusters: dict[VertexCluster, TimeRange] = {VertexCluster(): TimeRange(t, t)}

    new_element = Factory.create(graph2, clusters, measurement)
    graph2.add_element(new_element)

    assert len(graph2.vertex_storage.vertices) == 2
    assert len(graph2.edges) == 3
    assert len(graph2.vertex_storage.clusters) == 2
    assert len(graph2.connections) == 2
    for edges in graph2.connections.values():
        assert len(edges) == 2


def test_create_graph_element_with_0_new_vertices_for_1_existing(graph1):
    t = 1
    measurement = PoseOdometry(t, TimeRange(0, t), identity4x4, identity3x3, identity3x3, [])
    clusters: dict[VertexCluster, TimeRange] = {VertexCluster(): TimeRange(t, t)}

    new_element = Factory.create(graph1, clusters, measurement)
    graph1.add_element(new_element)

    assert len(graph1.vertex_storage.vertices) == 2
    assert len(graph1.edges) == 2
    assert len(graph1.vertex_storage.clusters) == 2
    assert len(graph1.connections) == 2


def test_create_2_graph_elements_with_0_new_for_2_existing(graph2):
    t = 1
    measurement1 = PoseOdometry(t, TimeRange(0, t), identity4x4, identity3x3, identity3x3, [])
    measurement2 = PoseOdometry(t, TimeRange(0, t), identity4x4, identity3x3, identity3x3, [])
    clusters: dict[VertexCluster, TimeRange] = {VertexCluster(): TimeRange(t, t)}

    new_element1 = Factory.create(graph2, clusters, measurement1)
    graph2.add_element(new_element1)
    new_element2 = Factory.create(graph2, clusters, measurement2)
    graph2.add_element(new_element2)

    assert len(graph2.vertex_storage.vertices) == 2
    assert len(graph2.edges) == 4
    assert len(graph2.vertex_storage.clusters) == 2
    assert len(graph2.connections) == 2


def test_create_2_graph_elements_with_1_new_for_1_existing(graph1):
    t1, t2 = 1, 2

    measurement1 = PoseOdometry(t1, TimeRange(0, t1), identity4x4, identity3x3, identity3x3, [])
    measurement2 = PoseOdometry(t2, TimeRange(0, t2), identity4x4, identity3x3, identity3x3, [])
    clusters: dict[VertexCluster, TimeRange] = {VertexCluster(): TimeRange(t1, t2)}

    new_element1 = Factory.create(graph1, clusters, measurement1)
    graph1.add_element(new_element1)
    new_element2 = Factory.create(graph1, clusters, measurement2)
    graph1.add_element(new_element2)

    assert len(graph1.vertex_storage.vertices) == 2
    assert len(graph1.edges) == 3
    assert len(graph1.vertex_storage.clusters) == 2
    assert len(graph1.connections) == 2


def test_create_graph_element_with_1_new_vertex_for_2_existing(graph2):
    t = 2
    measurement = PoseOdometry(t, TimeRange(0, t), identity4x4, identity3x3, identity3x3, [])
    clusters: dict[VertexCluster, TimeRange] = {VertexCluster(): TimeRange(t, t)}

    new_element = Factory.create(graph2, clusters, measurement)
    graph2.add_element(new_element)

    assert len(graph2.vertex_storage.vertices) == 3
    assert len(graph2.edges) == 3
    assert len(graph2.vertex_storage.clusters) == 3
    assert len(graph2.connections) == 3


def test_create_graph_element_with_1_new_vertex_for_1_existing(graph1):
    t = 1
    measurement = PoseOdometry(t, TimeRange(0, t), identity4x4, identity3x3, identity3x3, [])
    clusters: dict[VertexCluster, TimeRange] = {VertexCluster(): TimeRange(t, t)}

    new_element = Factory.create(graph1, clusters, measurement)
    graph1.add_element(new_element)

    assert len(graph1.vertex_storage.vertices) == 2
    assert len(graph1.edges) == 2
    assert len(graph1.vertex_storage.clusters) == 2
    assert len(graph1.connections) == 2


def test_create_2_graph_elements_with_1_new_vertex_for_2_existing(graph2):
    measurement1 = PoseOdometry(2, TimeRange(0, 2), identity4x4, identity3x3, identity3x3, [])
    measurement2 = PoseOdometry(3, TimeRange(1, 3), identity4x4, identity3x3, identity3x3, [])
    clusters: dict[VertexCluster, TimeRange] = {VertexCluster(): TimeRange(2, 3)}

    new_element = Factory.create(graph2, clusters, measurement1)
    graph2.add_element(new_element)
    new_element = Factory.create(graph2, clusters, measurement2)
    graph2.add_element(new_element)

    assert len(graph2.vertex_storage.vertices) == 3
    assert len(graph2.edges) == 4
    assert len(graph2.vertex_storage.clusters) == 3
    assert len(graph2.connections) == 3


def test_create_2_graph_elements_with_1_new_vertex_for_1_existing(graph1):
    measurement1 = PoseOdometry(1, TimeRange(0, 1), identity4x4, identity3x3, identity3x3, [])
    measurement2 = PoseOdometry(2, TimeRange(0, 2), identity4x4, identity3x3, identity3x3, [])
    clusters: dict[VertexCluster, TimeRange] = {VertexCluster(): TimeRange(1, 2)}

    new_element = Factory.create(graph1, clusters, measurement1)
    graph1.add_element(new_element)
    new_element = Factory.create(graph1, clusters, measurement2)
    graph1.add_element(new_element)

    assert len(graph1.vertex_storage.vertices) == 2
    assert len(graph1.edges) == 3
    assert len(graph1.vertex_storage.clusters) == 2
    assert len(graph1.connections) == 2


def test_create_2_graph_elements_with_2_new_vertices_for_2_existing(graph2):
    measurement1 = PoseOdometry(2, TimeRange(0, 2), identity4x4, identity3x3, identity3x3, [])
    measurement2 = PoseOdometry(3, TimeRange(1, 3), identity4x4, identity3x3, identity3x3, [])
    clusters: dict[VertexCluster, TimeRange] = {
        VertexCluster(): TimeRange(2, 2),
        VertexCluster(): TimeRange(3, 3),
    }

    new_element = Factory.create(graph2, clusters, measurement1)
    graph2.add_element(new_element)
    new_element = Factory.create(graph2, clusters, measurement2)
    graph2.add_element(new_element)

    assert len(graph2.vertex_storage.vertices) == 4
    assert len(graph2.edges) == 4
    assert len(graph2.vertex_storage.clusters) == 4
    assert len(graph2.connections) == 4


def test_create_2_graph_elements_with_2_new_vertices_for_1_existing(graph1):
    measurement1 = PoseOdometry(1, TimeRange(0, 1), identity4x4, identity3x3, identity3x3, [])
    measurement2 = PoseOdometry(2, TimeRange(1, 2), identity4x4, identity3x3, identity3x3, [])
    clusters: dict[VertexCluster, TimeRange] = {
        VertexCluster(): TimeRange(1, 1),
        VertexCluster(): TimeRange(2, 2),
    }

    new_element = Factory.create(graph1, clusters, measurement1)
    graph1.add_element(new_element)
    new_element = Factory.create(graph1, clusters, measurement2)
    graph1.add_element(new_element)

    assert len(graph1.vertex_storage.vertices) == 3
    assert len(graph1.edges) == 3
    assert len(graph1.vertex_storage.clusters) == 3
    assert len(graph1.connections) == 3
