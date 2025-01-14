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


def test_empty_graph(graph0: Graph):
    t = 0
    measurement = PoseMeasurement(t, i4x4, i3x3, i3x3)
    cluster = VertexCluster()
    clusters = {cluster: TimeRange(t, t)}

    element = Factory.create(graph0, clusters, measurement)

    assert element.edge.index is None
    assert len(element.new_vertices) == 1
    new_v = element.new_vertices[0]
    pose = new_v.instance

    assert new_v.cluster is cluster
    assert pose.index == 0
    assert new_v.timestamp == t
    assert element.edge.vertex is pose
    assert element.vertex_timestamp_table == {pose: t}


def test_0_new_vertices(graph1: Graph):
    t = 0
    measurement = PoseMeasurement(t, i4x4, i3x3, i3x3)
    cluster = VertexCluster()
    clusters = {cluster: TimeRange(t, t)}
    existing_pose = graph1.vertex_storage.get_last_vertex(Pose)

    element = Factory.create(graph1, clusters, measurement)

    assert element.edge.index is None
    assert not element.new_vertices
    assert element.edge.vertex is existing_pose
    assert element.vertex_timestamp_table == {existing_pose: t}


def test_1_existing_1_new_vertex(graph1: Graph):
    t = 1
    measurement = PoseMeasurement(t, i4x4, i3x3, i3x3)
    cluster = VertexCluster()
    clusters = {cluster: TimeRange(t, t)}
    existing_pose = graph1.vertex_storage.get_last_vertex(Pose)

    element = Factory.create(graph1, clusters, measurement)

    assert element.edge.index is None
    assert len(element.new_vertices) == 1

    new_v = element.new_vertices[0]
    pose = new_v.instance

    assert new_v.cluster is cluster
    assert pose is not existing_pose
    assert pose.index == 1
    assert new_v.timestamp == t
    assert element.vertex_timestamp_table == {pose: t}


def test_2_existing_0_new_vertex(graph2: Graph):
    t = 1
    measurement = PoseMeasurement(t, i4x4, i3x3, i3x3)
    cluster = VertexCluster()
    clusters = {cluster: TimeRange(t, t)}
    existing_p1 = graph2.vertex_storage.vertices[0]
    existing_p2 = graph2.vertex_storage.vertices[1]

    element = Factory.create(graph2, clusters, measurement)

    v = element.edge.vertex

    assert element.edge.index is None
    assert len(element.new_vertices) == 0
    assert v is existing_p2
    assert v is not existing_p1
    assert element.vertex_timestamp_table == {v: t}


def test_2_existing_1_new_vertex(graph2: Graph):
    t = 2
    measurement = PoseMeasurement(t, i4x4, i3x3, i3x3)
    cluster = VertexCluster()
    clusters = {cluster: TimeRange(t, t)}
    existing_v1 = graph2.vertex_storage.vertices[0]
    existing_v2 = graph2.vertex_storage.vertices[1]

    element = Factory.create(graph2, clusters, measurement)

    assert len(element.new_vertices) == 1

    new_v = element.new_vertices[0]
    v = element.edge.vertex

    assert new_v.cluster is cluster
    assert v is new_v.instance
    assert element.edge.index is None
    assert v is not existing_v2
    assert v is not existing_v1
    assert element.vertex_timestamp_table == {v: t}


def test_existing_0_new_vertex_wide_time_range(graph2: Graph):
    t1, t2 = 0, 1
    measurement = PoseMeasurement(t2, i4x4, i3x3, i3x3)
    clusters = {VertexCluster(): TimeRange(t1, t2)}
    existing_v1 = graph2.vertex_storage.vertices[0]
    existing_v2 = graph2.vertex_storage.vertices[1]

    element = Factory.create(graph2, clusters, measurement)

    assert not element.new_vertices

    v = element.edge.vertex

    assert element.edge.index is None
    assert v is existing_v2
    assert v is not existing_v1
    assert element.vertex_timestamp_table == {v: t2}
