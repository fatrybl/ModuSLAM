from moduslam.bridge.edge_factories.pose_odometry import Factory
from moduslam.frontend_manager.main_graph.graph import Graph
from moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from moduslam.measurement_storage.measurements.pose_odometry import Odometry
from moduslam.utils.auxiliary_dataclasses import TimeRange
from moduslam.utils.auxiliary_objects import identity3x3 as i3x3
from moduslam.utils.auxiliary_objects import identity4x4 as i4x4


def test_no_new_vertices(graph1: Graph):
    t1, t2 = 0, 1
    measurement = Odometry(t2, TimeRange(t1, t2), i4x4, i3x3, i3x3)
    clusters: dict[VertexCluster, TimeRange] = {VertexCluster(): TimeRange(t2, t2)}
    existing_pose = graph1.vertex_storage.vertices[0]

    new_element = Factory.create(graph1, clusters, measurement)

    v1 = new_element.edge.vertex1
    v2 = new_element.edge.vertex2

    assert v1 is not v2
    assert len(new_element.new_vertices) == 1

    new_v = new_element.new_vertices[0]
    pose = new_v.instance

    assert v1 is existing_pose
    assert v2 is not existing_pose
    assert v2.index == 1
    assert pose is not existing_pose
    assert pose is v2
    assert new_v.cluster.empty is True
    assert new_v.timestamp == t2
    assert new_element.vertex_timestamp_table == {existing_pose: t1, pose: t2}


def test_no_new_vertices_for_2_existing(graph2: Graph):
    t1, t2 = 0, 1
    measurement = Odometry(t2, TimeRange(t1, t2), i4x4, i3x3, i3x3)
    clusters: dict[VertexCluster, TimeRange] = {VertexCluster(): TimeRange(t2, t2)}
    existing_pose1 = graph2.vertex_storage.vertices[0]
    existing_pose2 = graph2.vertex_storage.vertices[1]

    new_element = Factory.create(graph2, clusters, measurement)

    v1 = new_element.edge.vertex1
    v2 = new_element.edge.vertex2

    assert v1 is not v2
    assert not new_element.new_vertices
    assert v1 is existing_pose1
    assert v2 is existing_pose2
    assert new_element.vertex_timestamp_table == {v1: t1, v2: t2}


def test_with_2_new_vertices(graph0: Graph):
    t1, t2 = 0, 1
    cluster = VertexCluster()
    measurement = Odometry(t2, TimeRange(t1, t2), i4x4, i3x3, i3x3)
    clusters = {cluster: TimeRange(t2, t2)}

    new_element = Factory.create(graph0, clusters, measurement)

    assert len(new_element.new_vertices) == 2

    new_v1 = new_element.new_vertices[0]
    new_v2 = new_element.new_vertices[1]
    v1 = new_element.edge.vertex1
    v2 = new_element.edge.vertex2
    pose1 = new_v1.instance
    pose2 = new_v2.instance
    cluster1 = new_v1.cluster
    cluster2 = new_v2.cluster

    assert v1 is not v2
    assert v1.index == 0
    assert v2.index == 1
    assert pose1 is v1
    assert pose2 is v2
    assert cluster2 is cluster
    assert cluster1 is not cluster
    assert new_v1.timestamp == t1
    assert new_v2.timestamp == t2
    assert new_element.vertex_timestamp_table == {v1: t1, v2: t2}


def test_create_with_1_new_1_existing(graph1: Graph):
    t1, t2 = 0, 1
    cluster = VertexCluster()
    measurement = Odometry(t2, TimeRange(t1, t2), i4x4, i3x3, i3x3)
    clusters = {cluster: TimeRange(t2, t2)}
    existing_v = graph1.vertex_storage.vertices[0]

    new_element = Factory.create(graph1, clusters, measurement)

    assert len(new_element.new_vertices) == 1

    new_v = new_element.new_vertices[0]
    v1 = new_element.edge.vertex1
    v2 = new_element.edge.vertex2
    new_cluster = new_v.cluster
    pose = new_v.instance

    assert v1 is not v2
    assert new_cluster is cluster
    assert v1 is existing_v
    assert v2 is not existing_v
    assert v2 is pose
    assert v1.index == 0
    assert v2.index == 1
    assert new_v.timestamp == t2
    assert new_element.vertex_timestamp_table == {v1: t1, v2: t2}


def test_create_with_1_new_2_existing(graph2: Graph):
    t1, t2 = 0, 2
    measurement = Odometry(t2, TimeRange(t1, t2), i4x4, i3x3, i3x3)
    clusters: dict[VertexCluster, TimeRange] = {VertexCluster(): TimeRange(t2, t2)}
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
    assert new_element.vertex_timestamp_table == {v1: t1, v2: t2}


def test_create_with_2_new_2_existing(graph2: Graph):
    t1, t2 = 2, 3
    measurement1 = Odometry(t2, TimeRange(t1, t2), i4x4, i3x3, i3x3)
    clusters: dict[VertexCluster, TimeRange] = {VertexCluster(): TimeRange(t1, t2)}
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
    assert new_element1.vertex_timestamp_table == {v1: t1, v2: t2}
