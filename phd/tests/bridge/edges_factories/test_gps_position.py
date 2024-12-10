from phd.bridge.edge_factories.gps_position import Factory
from phd.measurement_storage.measurements.gps import Gps
from phd.moduslam.frontend_manager.main_graph.graph import Graph
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.frontend_manager.main_graph.vertices.custom import Pose
from phd.moduslam.utils.auxiliary_dataclasses import TimeRange
from phd.moduslam.utils.auxiliary_objects import identity3x3, zero_vector3


def test_create_empty_graph(empty_graph: Graph):
    t = 0
    cluster = VertexCluster()
    clusters = {cluster: TimeRange(t, t)}
    measurement = Gps(t, zero_vector3, identity3x3)

    element = Factory.create(empty_graph, clusters, measurement)

    edge_vertex = element.edge.vertex
    new_vertex = element.new_vertices[0]
    assert len(element.new_vertices) == 1
    assert new_vertex.instance.index == 0
    assert new_vertex.timestamp == t
    assert edge_vertex is new_vertex.instance


def test_create_graph_with_1_existing_vertex(graph1: Graph):
    t = 0
    clusters = {VertexCluster(): TimeRange(t, t)}
    existing_vertex = graph1.vertex_storage.get_last_vertex(Pose)
    measurement = Gps(t, zero_vector3, identity3x3)

    new_element = Factory.create(graph1, clusters, measurement)

    vertex = new_element.edge.vertex
    assert not new_element.new_vertices
    assert vertex is existing_vertex


def test_create_graph_with_1_existing_1_new_vertex(graph1: Graph):
    t = 1
    cluster = VertexCluster()
    clusters = {cluster: TimeRange(t, t)}
    existing_vertex = graph1.vertex_storage.get_last_vertex(Pose)
    measurement = Gps(t, zero_vector3, identity3x3)

    new_element = Factory.create(graph1, clusters, measurement)

    new_vertex = new_element.new_vertices[0]
    assert len(new_element.new_vertices) == 1
    assert new_vertex.instance is not existing_vertex
    assert new_vertex.instance.index == 1
    assert new_vertex.timestamp == t
