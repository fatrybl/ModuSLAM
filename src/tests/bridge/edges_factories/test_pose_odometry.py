from src.bridge.edge_factories.pose_odometry import Factory
from src.measurement_storage.measurements.pose_odometry import Odometry
from src.moduslam.frontend_manager.main_graph.graph import Graph
from src.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from src.utils.auxiliary_dataclasses import TimeRange
from src.utils.auxiliary_objects import identity3x3 as i3x3
from src.utils.auxiliary_objects import identity4x4 as i4x4


def test_create_element_no_new_vertices(graph1: Graph):
    t = 1
    measurement = Odometry(t, TimeRange(0, t), i4x4, i3x3, i3x3)
    clusters: dict[VertexCluster, TimeRange] = {VertexCluster(): TimeRange(t, t)}
    existing_v = graph1.vertex_storage.vertices[0]

    new_element = Factory.create(graph1, clusters, measurement)

    new_edge = new_element.edge
    v1 = new_edge.vertex1
    v2 = new_edge.vertex2

    assert v1 is not v2
    assert len(new_element.new_vertices) == 1

    new_v = new_element.new_vertices[0]
    new_pose = new_v.instance
    new_t = new_v.timestamp

    assert v1 is existing_v
    assert v2 is not existing_v
    assert v2.index == 1
    assert new_pose is not existing_v
    assert new_pose is v2
    assert new_v.cluster.empty is True
    assert new_t == t


def test_create_element_no_new_vertices_for_2_existing(graph2: Graph):
    t = 1
    measurement = Odometry(t, TimeRange(0, t), i4x4, i3x3, i3x3)
    clusters: dict[VertexCluster, TimeRange] = {VertexCluster(): TimeRange(t, t)}
    existing_v1 = graph2.vertex_storage.vertices[0]
    existing_v2 = graph2.vertex_storage.vertices[1]

    new_element = Factory.create(graph2, clusters, measurement)

    edge = new_element.edge
    v1 = edge.vertex1
    v2 = edge.vertex2

    assert v1 is not v2
    assert not new_element.new_vertices
    assert v1 is existing_v1
    assert v2 is existing_v2


def test_create_element_with_2_new_vertices(empty_graph: Graph):
    t = 1
    cluster = VertexCluster()
    measurement = Odometry(t, TimeRange(0, t), i4x4, i3x3, i3x3)
    clusters = {cluster: TimeRange(t, t)}

    new_element = Factory.create(empty_graph, clusters, measurement)

    assert len(new_element.new_vertices) == 2

    new_v1 = new_element.new_vertices[0]
    new_v2 = new_element.new_vertices[1]
    v1 = new_element.edge.vertex1
    v2 = new_element.edge.vertex2
    pose1 = new_v1.instance
    pose2 = new_v2.instance
    t1 = new_v1.timestamp
    t2 = new_v2.timestamp
    cluster1 = new_v1.cluster
    cluster2 = new_v2.cluster

    assert v1 is not v2
    assert v1.index == 0
    assert v2.index == 1
    assert pose1 is v1
    assert pose2 is v2
    assert cluster2 is cluster
    assert cluster1 is not cluster
    assert t1 == 0
    assert t2 == t


def test_create_graph_element_with_1_new_1_existing(graph1: Graph):
    t = 1
    cluster = VertexCluster()
    measurement = Odometry(t, TimeRange(0, t), i4x4, i3x3, i3x3)
    clusters = {cluster: TimeRange(t, t)}
    existing_v = graph1.vertex_storage.vertices[0]

    new_element = Factory.create(graph1, clusters, measurement)

    assert len(new_element.new_vertices) == 1

    new_v = new_element.new_vertices[0]
    v1 = new_element.edge.vertex1
    v2 = new_element.edge.vertex2
    new_cluster = new_v.cluster
    pose = new_v.instance
    t1 = new_v.timestamp

    assert v1 is not v2
    assert new_cluster is cluster
    assert v1 is existing_v
    assert v2 is not existing_v
    assert v2 is pose
    assert v1.index == 0
    assert v2.index == 1
    assert t1 == t


def test_create_graph_element_with_1_new_2_existing(graph2: Graph):
    t = 2
    measurement = Odometry(t, TimeRange(0, t), i4x4, i3x3, i3x3)
    clusters: dict[VertexCluster, TimeRange] = {VertexCluster(): TimeRange(t, t)}
    existing_v1 = graph2.vertex_storage.vertices[0]
    existing_v2 = graph2.vertex_storage.vertices[1]

    new_element = Factory.create(graph2, clusters, measurement)

    edge = new_element.edge
    v1 = edge.vertex1
    v2 = edge.vertex2

    assert v1 is not v2
    assert len(new_element.new_vertices) == 1
    assert v1 is existing_v1
    assert v2 is not existing_v2


def test_create_element_with_2_new_2_existing(graph2: Graph):
    measurement1 = Odometry(3, TimeRange(2, 3), i4x4, i3x3, i3x3)
    clusters: dict[VertexCluster, TimeRange] = {VertexCluster(): TimeRange(2, 3)}
    existing_v1 = graph2.vertex_storage.vertices[0]
    existing_v2 = graph2.vertex_storage.vertices[1]

    new_element1 = Factory.create(graph2, clusters, measurement1)

    edge1 = new_element1.edge
    v1 = edge1.vertex1
    v2 = edge1.vertex2

    assert len(new_element1.new_vertices) == 2
    assert v1 is not v2
    assert v1 is not existing_v1 and v1 is not existing_v2
    assert v2 is not existing_v1 and v2 is not existing_v2
    assert v1.index == 2
    assert v2.index == 3
