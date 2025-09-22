"""Tests create_graph_element() method with pose-odometry measurements."""

from moduslam.bridge.candidates_factory import create_graph_elements
from moduslam.frontend_manager.main_graph.graph import Graph
from moduslam.measurement_storage.cluster import MeasurementCluster
from moduslam.measurement_storage.measurements.auxiliary import SplitPoseOdometry
from moduslam.measurement_storage.measurements.pose import Pose as PoseMeasurement
from moduslam.measurement_storage.measurements.pose_odometry import Odometry
from moduslam.utils.auxiliary_dataclasses import TimeRange
from moduslam.utils.auxiliary_objects import identity3x3 as i3x3
from moduslam.utils.auxiliary_objects import identity4x4 as i4x4


def test_2_measurements_1_cluster(graph0: Graph):
    t1, t2 = 0, 1
    m1 = Odometry(t2, TimeRange(t1, t2), i4x4, i3x3, i3x3)
    m2 = Odometry(t2, TimeRange(t1, t2), i4x4, i3x3, i3x3)
    cluster = MeasurementCluster()
    cluster.add(m1)
    cluster.add(m2)

    elements = create_graph_elements(graph0, [cluster])

    assert len(elements) == 2

    elem1, elem2 = elements
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

    elem1, elem2 = elements
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


def test_with_3_measurements_2_clusters(graph0: Graph):
    t0, t1, t2, t3 = 0, 1, 2, 3
    m1 = PoseMeasurement(t1, i4x4, i3x3, i3x3)
    m2 = Odometry(t2, TimeRange(t0, t2), i4x4, i3x3, i3x3)
    m3 = Odometry(t3, TimeRange(t2, t3), i4x4, i3x3, i3x3)
    cluster1, cluster2 = MeasurementCluster(), MeasurementCluster()
    cluster1.add(m1)
    cluster1.add(m2)
    cluster2.add(m3)

    elements = create_graph_elements(graph0, [cluster1, cluster2])

    assert len(elements) == 3

    elem1, elem2, elem3 = elements

    assert elem1 is not elem2 and elem2 is not elem3 and elem1 is not elem3
    assert len(elem1.new_vertices) == len(elem2.new_vertices) == len(elem3.new_vertices) == 1

    clusters = graph0.vertex_storage.clusters

    assert len(clusters) == 3

    cls1, cls2, cls3 = clusters
    v1, v2, v3 = cls1.vertices[0], cls2.vertices[0], cls3.vertices[0]

    assert cls1.time_range == TimeRange(t1, t2)
    assert cls2.time_range == TimeRange(t0, t0)
    assert cls3.time_range == TimeRange(t3, t3)
    assert cls1.vertices_with_timestamps == {v1: {t1: 1, t2: 2}}
    assert cls2.vertices_with_timestamps == {v2: {t0: 1}}
    assert cls3.vertices_with_timestamps == {v3: {t3: 1}}

    sorted_clusters = graph0.vertex_storage.sorted_clusters
    cls1, cls2, cls3 = sorted_clusters

    assert len(cls1.vertices) == len(cls2.vertices) == len(cls3.vertices) == 1

    v1, v2, v3 = cls1.vertices[0], cls2.vertices[0], cls3.vertices[0]

    assert len(graph0.edges) == 3
    assert cls1.time_range == TimeRange(t0, t0)
    assert cls2.time_range == TimeRange(t1, t2)
    assert cls3.time_range == TimeRange(t3, t3)
    assert cls1.vertices_with_timestamps == {v1: {t0: 1}}
    assert cls2.vertices_with_timestamps == {v2: {t1: 1, t2: 2}}
    assert cls3.vertices_with_timestamps == {v3: {t3: 1}}


def test_3_measurements_1_cluster(graph2: Graph):
    t0, t1 = 0, 1
    m1 = Odometry(t1, TimeRange(t0, t1), i4x4, i3x3, i3x3)
    m2 = Odometry(t1, TimeRange(t0, t1), i4x4, i3x3, i3x3)
    cluster = MeasurementCluster()
    cluster.add(m1)
    cluster.add(m2)
    existing_pose1, existing_pose2 = graph2.vertex_storage.vertices

    elements = create_graph_elements(graph2, [cluster])

    assert len(elements) == 2

    elem1, elem2 = elements
    e1, e2 = elem1.edge, elem2.edge

    assert elem1 is not elem2
    assert len(elem1.new_vertices) == 0
    assert len(elem2.new_vertices) == 0

    assert e1 is not e2
    assert e1.index == 2
    assert e2.index == 3

    assert existing_pose1 is e1.vertices[0] and existing_pose2 is e1.vertices[1]
    assert existing_pose1 is e2.vertices[0] and existing_pose2 is e2.vertices[1]
    assert len(graph2.vertex_storage.clusters) == 2

    cls1, cls2 = graph2.vertex_storage.clusters

    assert cls1.time_range == TimeRange(t0, t0)
    assert cls2.time_range == TimeRange(t1, t1)
    assert cls1.vertices_with_timestamps == {existing_pose1: {t0: 3}}
    assert cls2.vertices_with_timestamps == {existing_pose2: {t1: 3}}

    cls1, cls2 = graph2.vertex_storage.sorted_clusters

    assert cls1.time_range == TimeRange(t0, t0)
    assert cls2.time_range == TimeRange(t1, t1)
    assert cls1.vertices_with_timestamps == {existing_pose1: {t0: 3}}
    assert cls2.vertices_with_timestamps == {existing_pose2: {t1: 3}}


def test_2_measurements_3_clusters(graph0: Graph):
    t0, t1, t2 = 0, 1, 2
    m1 = PoseMeasurement(t1, i4x4, i3x3, i3x3)
    m2 = Odometry(t2, TimeRange(t0, t2), i4x4, i3x3, i3x3)
    cluster1, cluster2 = MeasurementCluster(), MeasurementCluster()
    cluster1.add(m1)
    cluster2.add(m2)

    elements = create_graph_elements(graph0, [cluster1, cluster2])

    assert len(elements) == 2

    elem1, elem2 = elements
    e1, e2 = elem1.edge, elem2.edge

    assert e1 is not e2
    assert e1.index == 0
    assert e2.index == 1

    assert elem1 is not elem2
    assert len(elem1.new_vertices) == 1
    assert len(elem2.new_vertices) == 2
    assert len(graph0.vertex_storage.vertices) == 3
    assert len(graph0.vertex_storage.clusters) == 3

    cls1, cls2, cls3 = graph0.vertex_storage.clusters
    pose1, pose2, pose3 = graph0.vertex_storage.vertices

    assert pose1 is e1.vertices[0]
    assert pose2 is e2.vertices[0] and pose3 is e2.vertices[1]
    assert cls1.time_range == TimeRange(t1, t1)
    assert cls2.time_range == TimeRange(t0, t0)
    assert cls3.time_range == TimeRange(t2, t2)
    assert cls1.vertices_with_timestamps == {pose1: {t1: 1}}
    assert cls2.vertices_with_timestamps == {pose2: {t0: 1}}
    assert cls3.vertices_with_timestamps == {pose3: {t2: 1}}

    cls1, cls2, cls3 = graph0.vertex_storage.sorted_clusters

    assert cls1.time_range == TimeRange(t0, t0)
    assert cls2.time_range == TimeRange(t1, t1)
    assert cls3.time_range == TimeRange(t2, t2)
    assert cls1.vertices_with_timestamps == {pose2: {t0: 1}}
    assert cls2.vertices_with_timestamps == {pose1: {t1: 1}}
    assert cls3.vertices_with_timestamps == {pose3: {t2: 1}}


def test_split_odometry_3_clusters(graph2: Graph):
    t0, t1, t2 = 0, 1, 2
    odom = Odometry(t2, TimeRange(t1, t2), i4x4, i3x3, i3x3)
    m1 = SplitPoseOdometry(t1, odom)
    m2 = SplitPoseOdometry(t2, odom)
    cluster1, cluster2 = MeasurementCluster(), MeasurementCluster()
    cluster1.add(m1)
    cluster2.add(m2)

    elements = create_graph_elements(graph2, [cluster1, cluster2])

    assert len(elements) == 1

    elem = elements[0]
    e = elem.edge

    assert e.index == 2

    assert len(elem.new_vertices) == 1
    assert len(graph2.vertex_storage.vertices) == 3
    assert len(graph2.vertex_storage.clusters) == 3

    pose1, pose2, pose3 = graph2.vertex_storage.vertices
    cls1, cls2, cls3 = graph2.vertex_storage.clusters

    assert len(e.vertices) == 2
    assert pose2 is e.vertices[0]
    assert pose3 is e.vertices[1]

    assert cls1.time_range == TimeRange(t0, t0)
    assert cls2.time_range == TimeRange(t1, t1)
    assert cls3.time_range == TimeRange(t2, t2)
    assert cls1.vertices_with_timestamps == {pose1: {t0: 1}}
    assert cls2.vertices_with_timestamps == {pose2: {t1: 2}}
    assert cls3.vertices_with_timestamps == {pose3: {t2: 1}}
