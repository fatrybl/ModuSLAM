from phd.bridge.edge_factories.pose_odometry import Factory
from phd.measurement_storage.measurements.pose_odometry import Odometry
from phd.moduslam.frontend_manager.main_graph.graph import Graph
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.utils.auxiliary_dataclasses import TimeRange
from phd.utils.auxiliary_objects import identity3x3 as i3x3
from phd.utils.auxiliary_objects import identity4x4 as i4x4


def test_create_graph_element_with_2_new_vertices_for_empty_graph(empty_graph: Graph):
    cluster = VertexCluster()
    t = 1
    measurement = Odometry(t, TimeRange(0, t), i4x4, i3x3, i3x3)
    clusters = {cluster: TimeRange(t, t)}

    new_element = Factory.create(empty_graph, clusters, measurement)

    edge_vertex1 = new_element.edge.vertex1
    edge_vertex2 = new_element.edge.vertex2
    new_vertex1 = new_element.new_vertices[0]
    new_vertex2 = new_element.new_vertices[1]
    pose1 = new_vertex1.instance
    pose2 = new_vertex2.instance
    t1 = new_vertex1.timestamp
    t2 = new_vertex2.timestamp
    cluster1 = new_vertex1.cluster
    cluster2 = new_vertex2.cluster

    assert len(new_element.new_vertices) == 2
    assert edge_vertex1.index == 0
    assert edge_vertex2.index == 1
    assert pose1 is edge_vertex1
    assert pose2 is edge_vertex2
    assert cluster2 is cluster
    assert cluster1 is not cluster
    assert t1 == 0
    assert t2 == t


def test_create_graph_element_with_1_new_vertex_for_1_existing(graph1):
    t = 1
    cluster = VertexCluster()
    measurement = Odometry(t, TimeRange(0, t), i4x4, i3x3, i3x3)
    clusters = {cluster: TimeRange(t, t)}

    new_element = Factory.create(graph1, clusters, measurement)

    new_vertex = new_element.new_vertices[0]
    edge_vertex1 = new_element.edge.vertex1
    edge_vertex2 = new_element.edge.vertex2
    new_cluster = new_vertex.cluster
    pose1 = new_vertex.instance
    t1 = new_vertex.timestamp

    assert len(new_element.new_vertices) == 1

    existing_vertex = graph1.vertex_storage.vertices[0]

    assert new_cluster is cluster
    assert edge_vertex1 is existing_vertex
    assert edge_vertex2 is not existing_vertex
    assert edge_vertex2 is pose1
    assert edge_vertex1.index == 0
    assert edge_vertex2.index == 1
    assert t1 == t


def test_create_graph_element_with_0_new_vertices_for_2_existing(graph2: Graph):
    t = 1
    measurement = Odometry(t, TimeRange(0, t), i4x4, i3x3, i3x3)
    clusters: dict[VertexCluster, TimeRange] = {VertexCluster(): TimeRange(t, t)}

    new_element = Factory.create(graph2, clusters, measurement)

    edge_vertex1 = new_element.edge.vertex1
    edge_vertex2 = new_element.edge.vertex2

    existing_vertex1 = graph2.vertex_storage.vertices[0]
    existing_vertex2 = graph2.vertex_storage.vertices[1]

    assert not new_element.new_vertices
    assert edge_vertex1 is existing_vertex1
    assert edge_vertex2 is existing_vertex2
