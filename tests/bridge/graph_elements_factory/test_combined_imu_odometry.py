"""Tests create_graph_element() method with imu odometry measurements and combinedImu
factors.

Warning:
    all measurements of equal time must be added to Measurement Clusters.
    Do not add them to graph before calling create_graph_elements() method.
    There should not be the case when there are edges in the graph with measurements of t1, t2
    and one tries to test create_graph_elements() with new measurements of t1, t2 ...
"""

import pytest

from moduslam.bridge.candidates_factory import create_graph_elements
from moduslam.frontend_manager.main_graph.data_classes import NewVertex
from moduslam.frontend_manager.main_graph.edges.noise_models import (
    se3_isotropic_noise_model,
)
from moduslam.frontend_manager.main_graph.edges.pose import Pose as PriorPose
from moduslam.frontend_manager.main_graph.graph import Graph, GraphElement
from moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from moduslam.frontend_manager.main_graph.vertices.custom import Pose
from moduslam.measurement_storage.cluster import MeasurementCluster as Cluster
from moduslam.measurement_storage.measurements.auxiliary import SplitPoseOdometry
from moduslam.measurement_storage.measurements.imu import ContinuousImu
from moduslam.measurement_storage.measurements.pose import Pose as PoseMeasurement
from moduslam.measurement_storage.measurements.pose_odometry import Odometry
from moduslam.utils.auxiliary_dataclasses import TimeRange
from moduslam.utils.auxiliary_objects import identity3x3 as i3x3
from moduslam.utils.auxiliary_objects import identity4x4 as i4x4
from moduslam.utils.exceptions import ValidationError


@pytest.fixture
def graph2() -> Graph:
    """Graph with two poses."""
    graph = Graph()
    t1, t2 = 0, 3
    v1, v2 = Pose(0), Pose(1)
    noise = se3_isotropic_noise_model(1)
    m1, m2 = PoseMeasurement(t1, i4x4, i3x3, i3x3), PoseMeasurement(t2, i4x4, i3x3, i3x3)
    edge1, edge2 = PriorPose(v1, m1, noise), PriorPose(v2, m2, noise)
    cluster1, cluster2 = VertexCluster(), VertexCluster()
    element1 = GraphElement(edge1, {v1: t1}, (NewVertex(v1, cluster1, t1),))
    element2 = GraphElement(edge2, {v2: t2}, (NewVertex(v2, cluster2, t2),))
    graph.add_elements([element1, element2])
    return graph


def test_no_core_measurements(measurement: ContinuousImu, graph0: Graph):
    cluster = Cluster()
    cluster.add(measurement)

    with pytest.raises(ValidationError):
        _ = create_graph_elements(graph0, [cluster])


def test_empty_graph(measurement: ContinuousImu, graph0: Graph):
    t1, t2 = 0, 3
    m1 = PoseMeasurement(t1, i4x4, i3x3, i3x3)
    m2 = PoseMeasurement(t2, i4x4, i3x3, i3x3)
    cluster1, cluster2 = Cluster(), Cluster()
    cluster1.add(m1)
    cluster2.add(m2)
    cluster2.add(measurement)

    elements = create_graph_elements(graph0, [cluster1, cluster2])

    assert len(elements) == 3

    elem1, elem2, elem3 = elements
    clusters = graph0.vertex_storage.clusters

    assert len(clusters) == 2

    cls1, cls2 = clusters

    assert len(elem1.new_vertices) == len(elem2.new_vertices) == 1
    assert len(elem1.vertex_timestamp_table) == len(elem2.vertex_timestamp_table) == 1
    assert len(elem3.new_vertices) == 4
    assert len(elem3.vertex_timestamp_table) == 6

    assert cls1.time_range == TimeRange(t1, t1)
    assert cls2.time_range == TimeRange(t2, t2)

    assert len(graph0.vertex_storage.vertices) == 6
    assert len(cls1.vertices) == 3
    assert len(cls2.vertices) == 3

    p1, v1, b1 = cls1.vertices
    p2, v2, b2 = cls2.vertices

    assert cls1.vertices_with_timestamps == {p1: {t1: 2}, v1: {t1: 1}, b1: {t1: 1}}
    assert cls2.vertices_with_timestamps == {p2: {t2: 2}, v2: {t2: 1}, b2: {t2: 1}}


def test_non_empty_graph(measurement: ContinuousImu, graph2: Graph):
    t1, t2 = 0, 3
    m1 = PoseMeasurement(t2, i4x4, i3x3, i3x3)
    cluster = Cluster()
    cluster.add(m1)
    cluster.add(measurement)
    clusters = graph2.vertex_storage.clusters
    cls1, cls2 = clusters

    elements = create_graph_elements(graph2, [cluster])

    assert len(elements) == 2

    elem1, elem2 = elements

    assert len(elem1.new_vertices) == 0
    assert len(elem1.vertex_timestamp_table) == 1
    assert len(elem2.new_vertices) == 4
    assert len(elem2.vertex_timestamp_table) == 6

    assert cls1.time_range == TimeRange(t1, t1)
    assert cls2.time_range == TimeRange(t2, t2)

    assert len(graph2.vertex_storage.vertices) == 6
    assert len(cls1.vertices) == 3
    assert len(cls2.vertices) == 3

    p1, v1, b1 = cls1.vertices
    p2, v2, b2 = cls2.vertices

    assert cls1.vertices_with_timestamps == {p1: {t1: 2}, v1: {t1: 1}, b1: {t1: 1}}
    assert cls2.vertices_with_timestamps == {p2: {t2: 3}, v2: {t2: 1}, b2: {t2: 1}}


def test_with_odometry(measurement: ContinuousImu, graph0: Graph):
    t1, t2 = 0, 3
    m1 = Odometry(t2, TimeRange(t1, t2), i4x4, i3x3, i3x3)
    cluster = Cluster()
    cluster.add(m1)
    cluster.add(measurement)

    elements = create_graph_elements(graph0, [cluster])

    assert len(elements) == 2

    elem1, elem2 = elements
    clusters = graph0.vertex_storage.clusters

    assert len(clusters) == 2

    cls1, cls2 = clusters

    assert len(elem1.new_vertices) == 2
    assert len(elem2.new_vertices) == 4
    assert len(elem1.vertex_timestamp_table) == 2
    assert len(elem2.vertex_timestamp_table) == 6

    assert cls1.time_range == TimeRange(t1, t1)
    assert cls2.time_range == TimeRange(t2, t2)

    assert len(graph0.vertex_storage.vertices) == 6
    assert len(cls1.vertices) == 3
    assert len(cls2.vertices) == 3

    p1, v1, b1 = cls1.vertices
    p2, v2, b2 = cls2.vertices

    assert cls1.vertices_with_timestamps == {p1: {t1: 2}, v1: {t1: 1}, b1: {t1: 1}}
    assert cls2.vertices_with_timestamps == {p2: {t2: 2}, v2: {t2: 1}, b2: {t2: 1}}


def test_with_odometry_3_clusters(measurement: ContinuousImu, graph0: Graph):
    t0, t1, t2 = 0, 1, 3
    m1 = Odometry(t2, TimeRange(t1, t2), i4x4, i3x3, i3x3)
    cluster = Cluster()
    cluster.add(measurement)
    cluster.add(m1)

    elements = create_graph_elements(graph0, [cluster])

    assert len(elements) == 2
    assert len(graph0.vertex_storage.vertices) == 7

    elem1, elem2 = elements
    clusters = graph0.vertex_storage.clusters

    assert len(clusters) == 3

    cls1, cls2, cls3 = clusters

    assert len(elem1.new_vertices) == 2
    assert len(elem2.new_vertices) == 5
    assert len(elem1.vertex_timestamp_table) == 2
    assert len(elem2.vertex_timestamp_table) == 6

    assert cls1.time_range == TimeRange(t1, t1)
    assert cls2.time_range == TimeRange(t2, t2)
    assert cls3.time_range == TimeRange(t0, t0)

    assert len(cls1.vertices) == 1
    assert len(cls2.vertices) == 3
    assert len(cls3.vertices) == 3

    p1 = cls1.vertices[0]
    p2, v2, b2 = cls2.vertices
    p3, v3, b3 = cls3.vertices

    assert cls1.vertices_with_timestamps == {p1: {t1: 1}}
    assert cls2.vertices_with_timestamps == {p2: {t2: 2}, v2: {t2: 1}, b2: {t2: 1}}
    assert cls3.vertices_with_timestamps == {p3: {t0: 1}, v3: {t0: 1}, b3: {t0: 1}}

    sorted_clusters = graph0.vertex_storage.sorted_clusters
    cls1, cls2, cls3 = sorted_clusters

    assert cls1.time_range == TimeRange(t0, t0)
    assert cls2.time_range == TimeRange(t1, t1)
    assert cls3.time_range == TimeRange(t2, t2)

    assert len(cls1.vertices) == 3
    assert len(cls2.vertices) == 1
    assert len(cls3.vertices) == 3

    p1, v1, b1 = cls1.vertices
    p2 = cls2.vertices[0]
    p3, v3, b3 = cls3.vertices

    assert cls1.vertices_with_timestamps == {p1: {t0: 1}, v1: {t0: 1}, b1: {t0: 1}}
    assert cls2.vertices_with_timestamps == {p2: {t1: 1}}
    assert cls3.vertices_with_timestamps == {p3: {t2: 2}, v3: {t2: 1}, b3: {t2: 1}}


def test_with_2_split_odometries(measurement: ContinuousImu, graph0: Graph):
    t0, t1, t2, t3 = 0, 1, 2, 3
    odom1 = Odometry(t2, TimeRange(t0, t2), i4x4, i3x3, i3x3)
    odom2 = Odometry(t3, TimeRange(t1, t3), i4x4, i3x3, i3x3)
    m1 = SplitPoseOdometry(t0, odom1)
    m2 = SplitPoseOdometry(t1, odom2)
    m3 = SplitPoseOdometry(t2, odom1)
    m4 = SplitPoseOdometry(t3, odom2)
    cluster1, cluster2, cluster3 = Cluster(), Cluster(), Cluster()
    cluster1.add(m1)
    cluster1.add(m2)
    cluster2.add(m3)
    cluster3.add(m4)
    cluster3.add(measurement)

    elements = create_graph_elements(graph0, [cluster1, cluster2, cluster3])

    assert len(elements) == 3
    assert len(graph0.vertex_storage.vertices) == 7

    elem1, elem2, elem3 = elements
    clusters = graph0.vertex_storage.clusters

    assert len(clusters) == 3

    cls1, cls2, cls3 = clusters

    assert len(elem1.new_vertices) == 2
    assert len(elem2.new_vertices) == 1
    assert len(elem3.new_vertices) == 4

    assert cls1.time_range == TimeRange(t0, t1)
    assert cls2.time_range == TimeRange(t2, t2)
    assert cls3.time_range == TimeRange(t3, t3)

    assert len(cls1.vertices) == 3
    assert len(cls2.vertices) == 1
    assert len(cls3.vertices) == 3

    p1, v1, b1 = cls1.vertices
    p2 = cls2.vertices[0]
    p3, v3, b3 = cls3.vertices

    assert cls1.vertices_with_timestamps == {p1: {t0: 2, t1: 1}, v1: {t0: 1}, b1: {t0: 1}}
    assert cls2.vertices_with_timestamps == {p2: {t2: 1}}
    assert cls3.vertices_with_timestamps == {p3: {t3: 2}, v3: {t3: 1}, b3: {t3: 1}}

    sorted_clusters = graph0.vertex_storage.sorted_clusters

    for cls, sorted_cls in zip(clusters, sorted_clusters):
        assert cls == sorted_cls


def test_with_2_split_odometries_2_poses(measurement: ContinuousImu, graph0: Graph):
    t0, t1, t2, t3 = 0, 1, 2, 3
    odom1 = Odometry(t2, TimeRange(t0, t2), i4x4, i3x3, i3x3)
    odom2 = Odometry(t3, TimeRange(t1, t3), i4x4, i3x3, i3x3)
    m1 = PoseMeasurement(t0, i4x4, i3x3, i3x3)
    m2 = PoseMeasurement(t2, i4x4, i3x3, i3x3)
    m3 = SplitPoseOdometry(t0, odom1)
    m4 = SplitPoseOdometry(t1, odom2)
    m5 = SplitPoseOdometry(t2, odom1)
    m6 = SplitPoseOdometry(t3, odom2)
    cluster1, cluster2, cluster3 = Cluster(), Cluster(), Cluster()
    for m in [m1, m3, m4]:
        cluster1.add(m)
    for m in [m2, m5]:
        cluster2.add(m)
    for m in [m6, measurement]:
        cluster3.add(m)

    elements = create_graph_elements(graph0, [cluster1, cluster2, cluster3])

    assert len(elements) == 5

    elem1, elem2, elem3, elem4, elem5 = elements

    assert len(graph0.vertex_storage.vertices) == 7

    clusters = graph0.vertex_storage.clusters

    assert len(clusters) == 3

    cls1, cls2, cls3 = clusters

    assert len(elem1.new_vertices) == 1
    assert len(elem2.new_vertices) == 1
    assert len(elem3.new_vertices) == 0
    assert len(elem4.new_vertices) == 1
    assert len(elem5.new_vertices) == 4

    assert cls1.time_range == TimeRange(t0, t1)
    assert cls2.time_range == TimeRange(t2, t2)
    assert cls3.time_range == TimeRange(t3, t3)

    assert len(cls1.vertices) == 3
    assert len(cls2.vertices) == 1
    assert len(cls3.vertices) == 3

    p1, v1, b1 = cls1.vertices
    p2 = cls2.vertices[0]
    p3, v3, b3 = cls3.vertices

    assert cls1.vertices_with_timestamps == {p1: {t0: 3, t1: 1}, v1: {t0: 1}, b1: {t0: 1}}
    assert cls2.vertices_with_timestamps == {p2: {t2: 2}}
    assert cls3.vertices_with_timestamps == {p3: {t3: 2}, v3: {t3: 1}, b3: {t3: 1}}

    sorted_clusters = graph0.vertex_storage.sorted_clusters

    for cls, sorted_cls in zip(clusters, sorted_clusters):
        assert cls == sorted_cls
