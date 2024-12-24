import gtsam.noiseModel
import pytest

from phd.measurement_storage.measurements.gps import Gps as GpsMeasurement
from phd.measurement_storage.measurements.pose import Pose as PoseMeasurement
from phd.moduslam.frontend_manager.main_graph.edges.gps_position import GpsPosition
from phd.moduslam.frontend_manager.main_graph.edges.pose import Pose as PriorPose
from phd.moduslam.frontend_manager.main_graph.graph import Graph, GraphElement
from phd.moduslam.frontend_manager.main_graph.new_element import NewVertex
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.frontend_manager.main_graph.vertices.custom import Pose as PoseVertex
from phd.utils.auxiliary_objects import identity3x3 as i3x3
from phd.utils.auxiliary_objects import identity4x4 as i4x4
from phd.utils.auxiliary_objects import zero_vector3
from phd.utils.exceptions import ValidationError


def test_replace_edge_raises_validation_error_when_edge_not_exists():
    t = 0
    graph = Graph()
    v = PoseVertex(t)
    noise_model = gtsam.noiseModel.Isotropic.Sigma(6, 1.0)
    prior_pose = PoseMeasurement(t, i4x4, i3x3, i3x3)
    e1 = PriorPose(v, prior_pose, noise_model)
    e2 = PriorPose(v, prior_pose, noise_model)

    with pytest.raises(ValidationError, match="Edge .* does not exist."):
        graph.replace_edge(e1, e2)


def test_replace_edge_raises_validation_error_when_new_edge_exists():
    graph = Graph()
    t = 0
    v = PoseVertex(t)
    cluster = VertexCluster()
    noise_model = gtsam.noiseModel.Isotropic.Sigma(6, 1.0)
    prior_pose = PoseMeasurement(t, i4x4, i3x3, i3x3)

    e1 = PriorPose(v, prior_pose, noise_model)
    e2 = PriorPose(v, prior_pose, noise_model)

    element1 = GraphElement(e1, [NewVertex(v, cluster, t)])
    element2 = GraphElement(e2, [])

    graph.add_element(element1)
    graph.add_element(element2)

    with pytest.raises(ValidationError, match="Edge .* already exists."):
        graph.replace_edge(e1, e2)


def test_replace_edge_raises_validation_error_for_incompatible_edge_types():
    t = 0
    graph = Graph()
    v = PoseVertex(t)
    cluster = VertexCluster()
    noise_model = gtsam.noiseModel.Isotropic.Sigma(6, 1.0)
    prior_pose = PoseMeasurement(t, i4x4, i3x3, i3x3)
    m = GpsMeasurement(0, zero_vector3, i3x3)

    e1 = PriorPose(v, prior_pose, noise_model)
    e2 = GpsPosition(v, m, noise_model)

    element1 = GraphElement(e1, [NewVertex(v, cluster, t)])
    graph.add_element(element1)

    with pytest.raises(
        ValidationError, match="Type mismatch between the existing edge and the new edge."
    ):
        graph.replace_edge(e1, e2)


def test_replace_edge_raises_validation_error_when_new_edge_vertices_not_subset():
    t1, t2 = 0, 1
    graph = Graph()
    v1 = PoseVertex(t1)
    v2 = PoseVertex(t2)
    cluster = VertexCluster()
    noise_model = gtsam.noiseModel.Isotropic.Sigma(6, 1.0)
    prior_pose = PoseMeasurement(t1, i4x4, i3x3, i3x3)

    e1 = PriorPose(v1, prior_pose, noise_model)
    e2 = PriorPose(v2, prior_pose, noise_model)

    element1 = GraphElement(e1, [NewVertex(v1, cluster, t1)])
    graph.add_element(element1)

    with pytest.raises(
        ValidationError, match="Vertices of the new edge do not match with the existing edge."
    ):
        graph.replace_edge(e1, e2)


def test_replace_edge():
    t = 0
    graph = Graph()
    v = PoseVertex(t)
    cluster = VertexCluster()
    noise_model = gtsam.noiseModel.Isotropic.Sigma(6, 1.0)
    prior_pose1 = PoseMeasurement(t, i4x4, i3x3, i3x3)
    prior_pose2 = PoseMeasurement(t, i4x4, i3x3, i3x3)
    e1 = PriorPose(v, prior_pose1, noise_model)
    e2 = PriorPose(v, prior_pose2, noise_model)
    element1 = GraphElement(e1, [NewVertex(v, cluster, t)])

    graph.add_element(element1)

    graph.replace_edge(e1, e2)

    assert len(graph.edges) == 1
    assert e1 not in graph.edges
    assert e2 in graph.edges
    assert v in graph.connections
    assert graph.factor_graph.nrFactors() == 1


def test_replace_edge_updates_connections_correctly():
    t = 0
    graph = Graph()
    v = PoseVertex(t)
    cluster = VertexCluster()
    noise_model = gtsam.noiseModel.Isotropic.Sigma(6, 1.0)
    prior_pose1 = PoseMeasurement(t, i4x4, i3x3, i3x3)
    prior_pose2 = PoseMeasurement(t, i4x4, i3x3, i3x3)
    e1 = PriorPose(v, prior_pose1, noise_model)
    e2 = PriorPose(v, prior_pose2, noise_model)
    element1 = GraphElement(e1, [NewVertex(v, cluster, t)])

    graph.add_element(element1)

    graph.replace_edge(e1, e2)

    assert e1 not in graph.connections[v]
    assert e2 in graph.connections[v]


def test_replace_edge_maintains_correct_index():
    t = 0
    graph = Graph()
    v = PoseVertex(t)
    cluster = VertexCluster()
    noise_model = gtsam.noiseModel.Isotropic.Sigma(6, 1.0)
    prior_pose1 = PoseMeasurement(t, i4x4, i3x3, i3x3)
    prior_pose2 = PoseMeasurement(t, i4x4, i3x3, i3x3)
    e1 = PriorPose(v, prior_pose1, noise_model)
    e2 = PriorPose(v, prior_pose2, noise_model)
    element1 = GraphElement(e1, [NewVertex(v, cluster, t)])

    graph.add_element(element1)
    original_index = e1.index

    graph.replace_edge(e1, e2)

    assert e2.index == original_index


def test_replace_edge_updates_factor_graph_correctly():
    t = 0
    graph = Graph()
    v = PoseVertex(t)
    cluster = VertexCluster()
    noise_model = gtsam.noiseModel.Isotropic.Sigma(6, 1.0)
    prior_pose1 = PoseMeasurement(t, i4x4, i3x3, i3x3)
    prior_pose2 = PoseMeasurement(t, i4x4, i3x3, i3x3)
    e1 = PriorPose(v, prior_pose1, noise_model)
    e2 = PriorPose(v, prior_pose2, noise_model)
    element1 = GraphElement(e1, [NewVertex(v, cluster, t)])

    graph.add_element(element1)
    old_factor = graph.factor_graph.at(e1.index)

    graph.replace_edge(e1, e2)

    new_factor = graph.factor_graph.at(e2.index)
    assert graph.factor_graph.exists(e2.index) is True
    assert old_factor is not new_factor
