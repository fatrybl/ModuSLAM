from phd.bridge.edge_factories.pose import Factory
from phd.measurements.processed_measurements import Pose as PoseMeasurement
from phd.moduslam.frontend_manager.main_graph.graph import Graph
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.frontend_manager.main_graph.vertices.custom import Pose
from phd.moduslam.utils.auxiliary_dataclasses import TimeRange
from phd.moduslam.utils.auxiliary_objects import identity3x3, identity4x4


def test_create_empty_graph():
    graph = Graph()
    measurement = PoseMeasurement(0, identity4x4, identity3x3, identity3x3, [])
    cluster = VertexCluster()
    clusters = {cluster: TimeRange(0, 0)}

    new_element = Factory.create(graph, clusters, measurement)
    edge_vertex = list(new_element.edge.vertices)[0]
    new_pose, timestamp = new_element.new_vertices[cluster][0]

    assert len(new_element.new_vertices) == 1
    assert new_pose.index == 0
    assert timestamp == 0
    assert edge_vertex is new_pose


def test_create_graph_with_1_existing_vertex(graph1: Graph):
    measurement = PoseMeasurement(0, identity4x4, identity3x3, identity3x3, [])
    cluster = VertexCluster()
    clusters = {cluster: TimeRange(0, 0)}
    existing_vertex = graph1.vertex_storage.get_latest_vertex(Pose)

    new_element = Factory.create(graph1, clusters, measurement)
    vertex = list(new_element.edge.vertices)[0]

    assert not new_element.new_vertices
    assert vertex is existing_vertex


def test_create_graph_with_1_existing_1_new_vertex(graph1: Graph):
    measurement = PoseMeasurement(1, identity4x4, identity3x3, identity3x3, [])
    cluster = VertexCluster()
    clusters = {cluster: TimeRange(1, 1)}
    existing_vertex = graph1.vertex_storage.get_latest_vertex(Pose)

    new_element = Factory.create(graph1, clusters, measurement)
    vertex, timestamp = new_element.new_vertices[cluster][0]

    assert len(new_element.new_vertices) == 1
    assert vertex is not existing_vertex
    assert vertex.index == 1
    assert timestamp == 1
