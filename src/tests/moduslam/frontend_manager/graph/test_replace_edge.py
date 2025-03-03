import pytest
from gtsam.noiseModel import Isotropic

from src.measurement_storage.measurements.pose import Pose as PoseMeasurement
from src.measurement_storage.measurements.position import Position as GpsMeasurement
from src.moduslam.frontend_manager.main_graph.data_classes import NewVertex
from src.moduslam.frontend_manager.main_graph.edges.gps_position import GpsPosition
from src.moduslam.frontend_manager.main_graph.edges.pose import Pose as PriorPose
from src.moduslam.frontend_manager.main_graph.graph import Graph, GraphElement
from src.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from src.moduslam.frontend_manager.main_graph.vertices.custom import Pose as PoseVertex
from src.utils.auxiliary_objects import identity3x3 as i3x3
from src.utils.auxiliary_objects import identity4x4 as i4x4
from src.utils.auxiliary_objects import zero_vector3
from src.utils.exceptions import ValidationError
from src.utils.ordered_set import OrderedSet


def test_raises_validation_error_when_edge_not_exists(noise: Isotropic):
    t = 0
    graph = Graph()
    v = PoseVertex(t)
    prior_pose = PoseMeasurement(t, i4x4, i3x3, i3x3)
    e1 = PriorPose(v, prior_pose, noise)
    e2 = PriorPose(v, prior_pose, noise)

    with pytest.raises(ValidationError):
        graph.replace_edge(e1, e2)


def test_raises_validation_error_edge_already_exists(noise: Isotropic):
    graph = Graph()
    t = 0
    v = PoseVertex(t)
    prior_pose = PoseMeasurement(t, i4x4, i3x3, i3x3)
    e1 = PriorPose(v, prior_pose, noise)
    e2 = PriorPose(v, prior_pose, noise)
    element1 = GraphElement(e1, {v: t}, (NewVertex(v, VertexCluster(), t),))
    element2 = GraphElement(e2, {v: t}, ())

    graph.add_element(element1)
    graph.add_element(element2)

    with pytest.raises(ValidationError):
        graph.replace_edge(e1, e2)


def test_raises_validation_error_incompatible_edge_types(noise: Isotropic):
    t = 0
    graph = Graph()
    v = PoseVertex(t)
    prior_pose = PoseMeasurement(t, i4x4, i3x3, i3x3)
    m = GpsMeasurement(0, zero_vector3, i3x3)

    e1 = PriorPose(v, prior_pose, noise)
    e2 = GpsPosition(v, m, noise)

    element1 = GraphElement(e1, {v: t}, (NewVertex(v, VertexCluster(), t),))
    graph.add_element(element1)

    with pytest.raises(ValidationError):
        graph.replace_edge(e1, e2)


def test_raises_validation_error_new_edge_vertices_is_not_subset(noise: Isotropic):
    t = 0
    graph = Graph()
    v1, v2 = PoseVertex(0), PoseVertex(1)
    prior_pose = PoseMeasurement(t, i4x4, i3x3, i3x3)

    e1 = PriorPose(v1, prior_pose, noise)
    e2 = PriorPose(v2, prior_pose, noise)

    element1 = GraphElement(e1, {v1: t}, (NewVertex(v1, VertexCluster(), t),))
    graph.add_element(element1)

    with pytest.raises(ValidationError):
        graph.replace_edge(e1, e2)


def test_no_exception(noise: Isotropic):
    t = 0
    graph = Graph()
    v = PoseVertex(t)
    prior_pose1 = PoseMeasurement(t, i4x4, i3x3, i3x3)
    prior_pose2 = PoseMeasurement(t, i4x4, i3x3, i3x3)
    e1 = PriorPose(v, prior_pose1, noise)
    e2 = PriorPose(v, prior_pose2, noise)
    element1 = GraphElement(e1, {v: t}, (NewVertex(v, VertexCluster(), t),))
    o_set = OrderedSet[PriorPose]()
    o_set.add(e2)

    graph.add_element(element1)

    graph.replace_edge(e1, e2)

    assert graph.edges == o_set
    assert e1 not in graph.edges
    assert e2 in graph.edges
    assert v in graph.connections
    assert graph.factor_graph.nrFactors() == 1


def test_updates_connections_correctly(noise: Isotropic):
    t = 0
    graph = Graph()
    v = PoseVertex(t)
    prior_pose1 = PoseMeasurement(t, i4x4, i3x3, i3x3)
    prior_pose2 = PoseMeasurement(t, i4x4, i3x3, i3x3)
    e1 = PriorPose(v, prior_pose1, noise)
    e2 = PriorPose(v, prior_pose2, noise)
    o_set = OrderedSet[PriorPose]()
    o_set.add(e2)
    element1 = GraphElement(e1, {v: t}, (NewVertex(v, VertexCluster(), t),))

    graph.add_element(element1)

    graph.replace_edge(e1, e2)

    assert e1 not in graph.connections[v]
    assert e2 in graph.connections[v]
    assert graph.edges == o_set


def test_maintains_correct_index(noise: Isotropic):
    t = 0
    graph = Graph()
    v = PoseVertex(t)
    prior_pose1 = PoseMeasurement(t, i4x4, i3x3, i3x3)
    prior_pose2 = PoseMeasurement(t, i4x4, i3x3, i3x3)
    e1 = PriorPose(v, prior_pose1, noise)
    e2 = PriorPose(v, prior_pose2, noise)
    element1 = GraphElement(e1, {v: t}, (NewVertex(v, VertexCluster(), t),))

    graph.add_element(element1)
    original_index = e1.index

    graph.replace_edge(e1, e2)

    assert e2.index == original_index


def test_replace_edge_updates_factor_graph_correctly(noise: Isotropic):
    t = 0
    graph = Graph()
    v = PoseVertex(t)
    prior_pose1 = PoseMeasurement(t, i4x4, i3x3, i3x3)
    prior_pose2 = PoseMeasurement(t, i4x4, i3x3, i3x3)
    e1 = PriorPose(v, prior_pose1, noise)
    e2 = PriorPose(v, prior_pose2, noise)
    element1 = GraphElement(e1, {v: t}, (NewVertex(v, VertexCluster(), t),))

    graph.add_element(element1)
    old_factor = graph.factor_graph.at(e1.index)

    graph.replace_edge(e1, e2)

    new_factor = graph.factor_graph.at(e2.index)
    assert graph.factor_graph.exists(e2.index) is True
    assert old_factor is not new_factor
