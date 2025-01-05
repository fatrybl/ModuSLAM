from src.bridge.edge_factories.pose import Factory
from src.measurement_storage.measurements.pose import Pose as PoseMeasurement
from src.moduslam.frontend_manager.main_graph.graph import Graph
from src.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from src.moduslam.frontend_manager.main_graph.vertices.custom import Pose
from src.utils.auxiliary_dataclasses import TimeRange
from src.utils.auxiliary_objects import identity3x3 as i3x3
from src.utils.auxiliary_objects import identity4x4 as i4x4


def test_create_empty_graph(empty_graph: Graph):
    t = 0
    measurement = PoseMeasurement(t, i4x4, i3x3, i3x3)
    cluster = VertexCluster()
    clusters = {cluster: TimeRange(t, t)}

    new_element = Factory.create(empty_graph, clusters, measurement)

    edge_vertex = new_element.edge.vertex
    new_vertex = new_element.new_vertices[0]
    new_pose = new_vertex.instance
    timestamp = new_vertex.timestamp
    assert len(new_element.new_vertices) == 1
    assert new_pose.index == 0
    assert timestamp == t
    assert edge_vertex is new_pose


def test_create_graph_with_1_existing_vertex(graph1: Graph):
    t = 0
    measurement = PoseMeasurement(t, i4x4, i3x3, i3x3)
    cluster = VertexCluster()
    clusters = {cluster: TimeRange(t, t)}
    existing_vertex = graph1.vertex_storage.get_last_vertex(Pose)

    new_element = Factory.create(graph1, clusters, measurement)

    vertex = new_element.edge.vertex
    assert not new_element.new_vertices
    assert vertex is existing_vertex


def test_create_graph_with_1_existing_1_new_vertex(graph1: Graph):
    t = 1
    measurement = PoseMeasurement(t, i4x4, i3x3, i3x3)
    cluster = VertexCluster()
    clusters = {cluster: TimeRange(t, t)}
    existing_pose = graph1.vertex_storage.get_last_vertex(Pose)

    new_element = Factory.create(graph1, clusters, measurement)

    new_vertex = new_element.new_vertices[0]
    pose = new_vertex.instance
    timestamp = new_vertex.timestamp
    assert len(new_element.new_vertices) == 1
    assert pose is not existing_pose
    assert pose.index == 1
    assert timestamp == t
