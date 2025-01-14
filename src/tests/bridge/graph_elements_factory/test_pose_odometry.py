"""Tests create_graph_element() method with pose-odometry measurements."""

import pytest

from src.bridge.candidates_factory import create_graph_elements
from src.bridge.distributor import distribution_table
from src.bridge.edge_factories.pose_odometry import Factory
from src.measurement_storage.cluster import MeasurementCluster
from src.measurement_storage.measurements.pose import Pose as PoseMeasurement
from src.measurement_storage.measurements.pose_odometry import Odometry
from src.moduslam.frontend_manager.main_graph.graph import Graph
from src.utils.auxiliary_dataclasses import TimeRange
from src.utils.auxiliary_objects import identity3x3 as i3x3
from src.utils.auxiliary_objects import identity4x4 as i4x4


@pytest.fixture(scope="module", autouse=True)
def add_factory_to_table():
    """Add the tested factory to the table of measurements` types and edge factories."""
    distribution_table.update({Odometry: Factory})


def test_2_measurements_1_cluster(graph0: Graph):
    t1, t2 = 0, 1
    m1 = Odometry(t2, TimeRange(t1, t2), i4x4, i3x3, i3x3)
    m2 = Odometry(t2, TimeRange(t1, t2), i4x4, i3x3, i3x3)
    cluster = MeasurementCluster()
    cluster.add(m1)
    cluster.add(m2)

    elements = create_graph_elements(graph0, [cluster])

    assert len(elements) == 2
    elem1, elem2 = elements[0], elements[1]
    e1, e2 = elem1.edge, elem2.edge

    assert elem1 is not elem2
    assert elem1.new_vertices != elem2.new_vertices
    assert len(elem1.new_vertices) == 2
    assert len(elem2.new_vertices) == 0

    assert e1 is not e2
    assert e1.index == 0
    assert e2.index == 1

    v1_1, v1_2 = elem1.new_vertices[0], elem1.new_vertices[1]
    assert v1_1 is not v1_2
    assert v1_1.timestamp == t1
    assert v1_2.timestamp == t2
    assert v1_1.instance.index == 0
    assert v1_2.instance.index == 1
    assert e1.vertices[0] is e2.vertices[0] is v1_1.instance
    assert e1.vertices[1] is e2.vertices[1] is v1_2.instance


def test_2_measurements_2_clusters(graph0: Graph):
    t1, t2, t3 = 0, 1, 2
    m1 = Odometry(t2, TimeRange(t1, t2), i4x4, i3x3, i3x3)
    m2 = Odometry(t3, TimeRange(t2, t3), i4x4, i3x3, i3x3)
    cluster1, cluster2 = MeasurementCluster(), MeasurementCluster()
    cluster1.add(m1)
    cluster2.add(m2)

    elements = create_graph_elements(graph0, [cluster1, cluster2])

    clusters = graph0.vertex_storage.clusters

    assert len(elements) == 2
    elem1, elem2 = elements[0], elements[1]
    e1, e2 = elem1.edge, elem2.edge

    assert elem1 is not elem2
    assert elem1.new_vertices != elem2.new_vertices
    assert len(elem1.new_vertices) == 2
    assert len(elem2.new_vertices) == 1
    v1_1, v1_2 = elem1.new_vertices[0], elem1.new_vertices[1]
    v2 = elem2.new_vertices[0]

    assert e1 is not e2
    assert e1.index == 0
    assert e2.index == 1
    assert e2.vertices[0] is v1_2.instance

    assert v1_1 is not v1_2
    assert v1_1.timestamp == t1
    assert v1_2.timestamp == t2
    assert v1_1.instance.index == 0
    assert v1_2.instance.index == 1
    assert v1_1.cluster is clusters[0]
    assert v1_2.cluster is clusters[1]

    assert v2.timestamp == t3
    assert v2.instance.index == 2
    assert v2.cluster is clusters[2]


def test_1_measurement(graph0: Graph):
    t0, t1, t2, t3 = 0, 1, 2, 3
    m1 = PoseMeasurement(t1, i4x4, i3x3, i3x3)
    m2 = Odometry(t2, TimeRange(t0, t2), i4x4, i3x3, i3x3)
    m3 = Odometry(t3, TimeRange(t2, t3), i4x4, i3x3, i3x3)
    cluster1, cluster2 = MeasurementCluster(), MeasurementCluster()
    cluster1.add(m1)
    cluster1.add(m2)
    cluster2.add(m3)

    elements = create_graph_elements(graph0, [cluster1])

    assert len(elements) == 2
    elem1, elem2 = elements[0], elements[1]

    assert elem1 is not elem2
    assert len(elem1.new_vertices) == len(elem2.new_vertices) == 1

    elements = create_graph_elements(graph0, [cluster2])

    assert len(elements) == 1
    elem3 = elements[0]

    assert len(elem3.new_vertices) == 1

    clusters = graph0.vertex_storage.sorted_clusters
    assert len(clusters) == 3
    cls1, cls2, cls3 = clusters[0], clusters[1], clusters[2]

    assert len(cls1.vertices) == len(cls2.vertices) == len(cls3.vertices) == 1

    v1, v2, v3 = cls1.vertices[0], cls2.vertices[0], cls3.vertices[0]

    assert len(graph0.edges) == 3
    assert cls1.time_range == TimeRange(t0, t0)
    assert cls2.time_range == TimeRange(t1, t2)
    assert cls3.time_range == TimeRange(t3, t3)
    assert cls1.vertices_with_timestamps == {v1: {t0: 1}}
    assert cls2.vertices_with_timestamps == {v2: {t1: 1, t2: 2}}
    assert cls3.vertices_with_timestamps == {v3: {t3: 1}}


# def test_2_measurements_equal_time(empty_graph: Graph):
#     m1 = PoseMeasurement(0, i4x4, i3x3, i3x3)
#     m2 = PoseMeasurement(0, i4x4, i3x3, i3x3)
#     cluster = MeasurementCluster()
#     cluster.add(m1)
#     cluster.add(m2)
#
#     elements = create_graph_elements(empty_graph, [cluster])
#
#     assert len(elements) == 2
#     elem1, elem2 = elements[0], elements[1]
#     e1, e2 = elem1.edge, elem2.edge
#
#     assert elem1 is not elem2
#     assert elem1.new_vertices != elem2.new_vertices
#     assert len(elem1.new_vertices) == 1
#     assert len(elem2.new_vertices) == 0
#     assert len(e1.vertices) == 1
#     assert len(e2.vertices) == 1
#     assert e1 is not e2
#     assert e1.index == 0
#     assert e2.index == 1
#
#     v1 = elem1.edge.vertices[0]
#     v2 = elem2.edge.vertices[0]
#
#     assert v1 is v2
#
#
# def test_2_measurements_equal_time_graph1(graph1: Graph):
#     m1 = PoseMeasurement(0, i4x4, i3x3, i3x3)
#     m2 = PoseMeasurement(0, i4x4, i3x3, i3x3)
#     cluster = MeasurementCluster()
#     cluster.add(m1)
#     cluster.add(m2)
#     existing_v = graph1.vertex_storage.get_last_vertex(Pose)
#
#     elements = create_graph_elements(graph1, [cluster])
#
#     assert len(elements) == 2
#     elem1, elem2 = elements[0], elements[1]
#     e1, e2 = elem1.edge, elem2.edge
#
#     assert elem1 is not elem2
#     assert elem1.new_vertices == elem2.new_vertices == []
#     assert len(e1.vertices) == 1
#     assert len(e2.vertices) == 1
#     assert e1 is not e2
#     assert e1.index == 1
#     assert e2.index == 2
#
#     v1 = elem1.edge.vertices[0]
#     v2 = elem2.edge.vertices[0]
#
#     assert v1 is v2 is existing_v
#
#
# def test_2_measurements_different_time(graph1: Graph):
#     m1 = PoseMeasurement(1, i4x4, i3x3, i3x3)
#     m2 = PoseMeasurement(2, i4x4, i3x3, i3x3)
#     cluster1, cluster2 = MeasurementCluster(), MeasurementCluster()
#     cluster1.add(m1)
#     cluster2.add(m2)
#     existing_v = graph1.vertex_storage.get_last_vertex(Pose)
#
#     elements = create_graph_elements(graph1, [cluster1, cluster2])
#
#     assert len(elements) == 2
#     elem1, elem2 = elements[0], elements[1]
#     e1, e2 = elem1.edge, elem2.edge
#
#     assert elem1 is not elem2
#     assert elem1.new_vertices != elem2.new_vertices
#     assert len(elem1.new_vertices) == 1
#     assert len(elem2.new_vertices) == 1
#
#     assert e1 is not e2
#     assert e1.index == 1
#     assert e2.index == 2
#
#     v1, v2 = elem1.new_vertices[0], elem2.new_vertices[0]
#     assert v1 is not v2
#     assert v1 is not existing_v and v2 is not existing_v
#     assert v1.timestamp == 1
#     assert v2.timestamp == 2
#     assert v1.instance.index == 1
#     assert v2.instance.index == 2
#     assert e1.vertex is v1.instance
#     assert e2.vertex is v2.instance
#
#
# def test_2_measurements_0_new_vertices(graph2: Graph):
#     m1 = PoseMeasurement(0, i4x4, i3x3, i3x3)
#     m2 = PoseMeasurement(1, i4x4, i3x3, i3x3)
#     cluster1, cluster2 = MeasurementCluster(), MeasurementCluster()
#     cluster1.add(m1)
#     cluster2.add(m2)
#     existing_v1 = graph2.vertex_storage.vertices[0]
#     existing_v2 = graph2.vertex_storage.vertices[1]
#
#     elements = create_graph_elements(graph2, [cluster1, cluster2])
#
#     assert len(elements) == 2
#     elem1, elem2 = elements[0], elements[1]
#     e1, e2 = elem1.edge, elem2.edge
#
#     assert elem1 is not elem2
#     assert elem1.new_vertices == elem2.new_vertices == []
#
#     assert e1 is not e2
#     assert e1.index == 2
#     assert e2.index == 3
#
#     v1 = elem1.edge.vertices[0]
#     v2 = elem2.edge.vertices[0]
#
#     assert v1 is not v2
#     assert v1 is existing_v1
#     assert v2 is existing_v2
#
#
# def test_2_measurements_1_new_vertex(graph2: Graph):
#     m1 = PoseMeasurement(1, i4x4, i3x3, i3x3)
#     m2 = PoseMeasurement(2, i4x4, i3x3, i3x3)
#     cluster1, cluster2 = MeasurementCluster(), MeasurementCluster()
#     cluster1.add(m1)
#     cluster2.add(m2)
#     existing_v1 = graph2.vertex_storage.vertices[0]
#     existing_v2 = graph2.vertex_storage.vertices[1]
#
#     elements = create_graph_elements(graph2, [cluster1, cluster2])
#
#     assert len(elements) == 2
#     elem1, elem2 = elements[0], elements[1]
#     e1, e2 = elem1.edge, elem2.edge
#
#     assert elem1 is not elem2
#     assert len(elem1.new_vertices) == 0
#     assert len(elem2.new_vertices) == 1
#
#     assert e1 is not e2
#     assert e1.index == 2
#     assert e2.index == 3
#
#     v1 = elem1.edge.vertices[0]
#     v2 = elem2.edge.vertices[0]
#
#     assert v1 is not v2
#     assert v1 is existing_v2
#     assert v2 is not existing_v1 and v2 is not existing_v2
#
#
# def test_2_measurements_2_new_vertices(graph2: Graph):
#     m1 = PoseMeasurement(2, i4x4, i3x3, i3x3)
#     m2 = PoseMeasurement(3, i4x4, i3x3, i3x3)
#     cluster1, cluster2 = MeasurementCluster(), MeasurementCluster()
#     cluster1.add(m1)
#     cluster2.add(m2)
#     existing_v1 = graph2.vertex_storage.vertices[0]
#     existing_v2 = graph2.vertex_storage.vertices[1]
#
#     elements = create_graph_elements(graph2, [cluster1, cluster2])
#
#     assert len(elements) == 2
#     elem1, elem2 = elements[0], elements[1]
#     e1, e2 = elem1.edge, elem2.edge
#
#     assert elem1 is not elem2
#     assert len(elem1.new_vertices) == 1
#     assert len(elem2.new_vertices) == 1
#
#     assert e1 is not e2
#     assert e1.index == 2
#     assert e2.index == 3
#
#     v1 = elem1.edge.vertices[0]
#     v2 = elem2.edge.vertices[0]
#
#     assert v1 is not v2
#     assert v1 is not existing_v1 and v1 is not existing_v2
#     assert v2 is not existing_v1 and v2 is not existing_v2
#     assert v1.index == 2
#     assert v2.index == 3
#
#
# def test_2_measurements_in_1_cluster_0_new_vertices(graph2: Graph):
#     m1 = PoseMeasurement(0, i4x4, i3x3, i3x3)
#     m2 = PoseMeasurement(1, i4x4, i3x3, i3x3)
#     cluster = MeasurementCluster()
#     cluster.add(m1)
#     cluster.add(m2)
#     existing_v1 = graph2.vertex_storage.vertices[0]
#     existing_v2 = graph2.vertex_storage.vertices[1]
#
#     elements = create_graph_elements(graph2, [cluster])
#
#     assert len(elements) == 2
#     elem1, elem2 = elements[0], elements[1]
#     e1, e2 = elem1.edge, elem2.edge
#
#     assert elem1 is not elem2
#     assert elem1.new_vertices == elem2.new_vertices == []
#
#     assert e1 is not e2
#     assert e1.index == 2
#     assert e2.index == 3
#
#     v1 = elem1.edge.vertices[0]
#     v2 = elem2.edge.vertices[0]
#
#     assert v1 is not v2
#     assert v1 is existing_v1
#     assert v2 is existing_v2
#
#
# def test_2_measurements_in_1_cluster_1_new_vertex(graph2: Graph):
#     m1 = PoseMeasurement(1, i4x4, i3x3, i3x3)
#     m2 = PoseMeasurement(2, i4x4, i3x3, i3x3)
#     cluster = MeasurementCluster()
#     cluster.add(m1)
#     cluster.add(m2)
#     existing_v2 = graph2.vertex_storage.vertices[1]
#
#     elements = create_graph_elements(graph2, [cluster])
#
#     assert len(elements) == 2
#     elem1, elem2 = elements[0], elements[1]
#     e1, e2 = elem1.edge, elem2.edge
#
#     assert elem1 is not elem2
#     assert not elem1.new_vertices
#     assert len(elem2.new_vertices) == 1
#
#     assert e1 is not e2
#     assert e1.index == 2
#     assert e2.index == 3
#
#     v1 = elem1.edge.vertices[0]
#     v2 = elem2.edge.vertices[0]
#
#     assert v1 is not v2
#     assert v1 is existing_v2
#     assert v2 is not existing_v2
