import pytest
from gtsam.noiseModel import Isotropic

from src.measurement_storage.measurements.pose import Pose as PoseMeasurement
from src.measurement_storage.measurements.pose_odometry import (
    Odometry as OdometryMeasurement,
)
from src.moduslam.frontend_manager.main_graph.data_classes import NewVertex
from src.moduslam.frontend_manager.main_graph.edges.pose import Pose as PriorPose
from src.moduslam.frontend_manager.main_graph.edges.pose_odometry import PoseOdometry
from src.moduslam.frontend_manager.main_graph.graph import Graph, GraphElement
from src.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from src.moduslam.frontend_manager.main_graph.vertices.custom import Pose as PoseVertex
from src.utils.auxiliary_dataclasses import TimeRange
from src.utils.auxiliary_objects import identity3x3 as i3x3
from src.utils.auxiliary_objects import identity4x4 as i4x4
from src.utils.exceptions import ValidationError


def test_add_element(noise: Isotropic):
    graph = Graph()
    t = 0
    v = PoseVertex(t)
    cluster = VertexCluster()
    measurement = PoseMeasurement(0, i4x4, i3x3, i3x3)
    e = PriorPose(v, measurement, noise)

    element = GraphElement(e, {v: t}, (NewVertex(v, cluster, t),))

    graph.add_element(element)

    assert len(graph.vertex_storage.clusters) == 1
    cls = graph.vertex_storage.clusters[0]
    assert cls.vertices_with_timestamps == {v: {t: 1}}
    assert e in graph.edges
    assert v in graph.connections
    assert e in graph.connections[v]
    assert graph.factor_graph.size() == 1


def test_add_elements(noise: Isotropic):
    graph = Graph()
    t1, t2 = 0, 1
    measurement1 = PoseMeasurement(t1, i4x4, i3x3, i3x3)
    measurement2 = PoseMeasurement(t2, i4x4, i3x3, i3x3)
    v1, v2 = PoseVertex(0), PoseVertex(1)
    cluster1, cluster2 = VertexCluster(), VertexCluster()
    e1 = PriorPose(v1, measurement1, noise)
    e2 = PriorPose(v2, measurement2, noise)
    element1 = GraphElement(e1, {v1: t1}, (NewVertex(v1, cluster1, t1),))
    element2 = GraphElement(e2, {v2: t2}, (NewVertex(v2, cluster2, t2),))

    graph.add_elements([element1, element2])

    assert e1 in graph.edges and e2 in graph.edges
    assert v1 in graph.connections and v2 in graph.connections
    assert e1 in graph.connections[v1]
    assert e2 in graph.connections[v2]
    assert graph.factor_graph.size() == 2

    clusters = graph.vertex_storage.clusters
    assert len(clusters) == 2
    cls1, cls2 = clusters[0], clusters[1]

    assert cls1.vertices_with_timestamps == {v1: {t1: 1}}
    assert cls2.vertices_with_timestamps == {v2: {t2: 1}}


def test_add_element_with_incorrect_new_vertex(noise: Isotropic):
    graph = Graph()
    t = 0
    v = PoseVertex(t)
    measurement = PoseMeasurement(t, i4x4, i3x3, i3x3)
    e = PriorPose(v, measurement, noise)
    element = GraphElement(e, {v: t}, ())

    with pytest.raises(ValidationError):
        graph.add_element(element)


def test_add_element_with_2nd_incorrect_new_vertex(noise: Isotropic):
    graph = Graph()
    cluster1, cluster2 = VertexCluster(), VertexCluster()
    t1, t2 = 0, 1
    measurement1 = PoseMeasurement(t1, i4x4, i3x3, i3x3)
    measurement2 = OdometryMeasurement(t2, TimeRange(t1, t2), i4x4, i3x3, i3x3)
    v1, v2 = PoseVertex(0), PoseVertex(1)
    e1 = PriorPose(v1, measurement1, noise)
    e2 = PoseOdometry(v1, v2, measurement2, noise)
    new_v1 = NewVertex(v1, cluster1, t1)
    new_v2 = NewVertex(v2, cluster2, t2)

    element1 = GraphElement(e1, {v1: t1}, (new_v1,))
    element2 = GraphElement(e2, {v1: t1, v2: t2}, (new_v1, new_v2))

    graph.add_element(element1)

    with pytest.raises(ValidationError):
        graph.add_element(element2)
