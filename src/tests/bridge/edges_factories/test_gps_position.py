from src.bridge.edge_factories.gps_position import Factory
from src.measurement_storage.measurements.position import Position
from src.moduslam.frontend_manager.main_graph.graph import Graph
from src.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from src.moduslam.frontend_manager.main_graph.vertices.custom import Pose
from src.utils.auxiliary_dataclasses import TimeRange
from src.utils.auxiliary_objects import identity3x3, zero_vector3


def test_create_empty_graph(graph0: Graph):
    t = 0
    cluster = VertexCluster()
    clusters = {cluster: TimeRange(t, t)}
    measurement = Position(t, zero_vector3, identity3x3)

    element = Factory.create(graph0, clusters, measurement)

    vertex = element.edge.vertex
    new_vertex = element.new_vertices[0]
    assert vertex is new_vertex.instance
    assert len(element.new_vertices) == 1
    assert new_vertex.instance.index == 0
    assert new_vertex.timestamp == t
    assert element.vertex_timestamp_table == {vertex: t}


def test_create_graph_with_1_existing_vertex(graph1: Graph):
    t = 0
    clusters = {VertexCluster(): TimeRange(t, t)}
    existing_vertex = graph1.vertex_storage.get_last_vertex(Pose)
    measurement = Position(t, zero_vector3, identity3x3)

    element = Factory.create(graph1, clusters, measurement)

    vertex = element.edge.vertex
    assert not element.new_vertices
    assert vertex is existing_vertex
    assert element.vertex_timestamp_table == {vertex: t}


def test_create_graph_with_1_existing_1_new_vertex(graph1: Graph):
    t = 1
    cluster = VertexCluster()
    clusters = {cluster: TimeRange(t, t)}
    existing_vertex = graph1.vertex_storage.get_last_vertex(Pose)
    measurement = Position(t, zero_vector3, identity3x3)

    element = Factory.create(graph1, clusters, measurement)

    new_vertex = element.new_vertices[0]
    vertex = element.edge.vertex
    assert len(element.new_vertices) == 1
    assert vertex is not existing_vertex
    assert vertex.index == 1
    assert new_vertex.timestamp == t
    assert element.vertex_timestamp_table == {vertex: t}
