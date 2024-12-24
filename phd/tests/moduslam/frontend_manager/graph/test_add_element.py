import gtsam.noiseModel
import pytest

from phd.measurement_storage.measurements.pose import Pose as PoseMeasurement
from phd.measurement_storage.measurements.pose_odometry import (
    Odometry as OdometryMeasurement,
)
from phd.moduslam.frontend_manager.main_graph.edges.pose import Pose as PriorPose
from phd.moduslam.frontend_manager.main_graph.edges.pose_odometry import PoseOdometry
from phd.moduslam.frontend_manager.main_graph.graph import Graph, GraphElement
from phd.moduslam.frontend_manager.main_graph.new_element import NewVertex
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.frontend_manager.main_graph.vertices.custom import Pose as PoseVertex
from phd.utils.auxiliary_dataclasses import TimeRange
from phd.utils.auxiliary_objects import identity3x3 as i3x3
from phd.utils.auxiliary_objects import identity4x4 as i4x4
from phd.utils.exceptions import ValidationError


def test_add_element():
    graph = Graph()
    t = 0
    v = PoseVertex(t)
    cluster = VertexCluster()
    noise_model = gtsam.noiseModel.Isotropic.Sigma(6, 1.0)
    measurement = PoseMeasurement(0, i4x4, i3x3, i3x3)
    e = PriorPose(v, measurement, noise_model)

    element = GraphElement(edge=e, new_vertices=[NewVertex(v, cluster, t)])

    graph.add_element(element)

    assert e in graph.edges
    assert v in graph.connections
    assert e in graph.connections[v]
    assert graph.factor_graph.size() == 1


def test_add_elements():
    graph = Graph()
    t1, t2 = 0, 1
    noise_model = gtsam.noiseModel.Isotropic.Sigma(6, 1.0)
    measurement1 = PoseMeasurement(t1, i4x4, i3x3, i3x3)
    measurement2 = PoseMeasurement(t2, i4x4, i3x3, i3x3)
    v1, v2 = PoseVertex(0), PoseVertex(1)
    cluster1, cluster2 = VertexCluster(), VertexCluster()
    e1 = PriorPose(v1, measurement1, noise_model)
    e2 = PriorPose(v2, measurement2, noise_model)
    element1 = GraphElement(edge=e1, new_vertices=[NewVertex(v1, cluster1, t1)])
    element2 = GraphElement(edge=e2, new_vertices=[NewVertex(v2, cluster2, t2)])

    graph.add_elements([element1, element2])

    assert e1 in graph.edges and e2 in graph.edges
    assert v1 in graph.connections and v2 in graph.connections
    assert e1 in graph.connections[v1]
    assert e2 in graph.connections[v2]

    assert graph.factor_graph.size() == 2


def test_add_element_with_incorrect_new_vertices_1():
    graph = Graph()
    t = 0
    v = PoseVertex(t)
    noise_model = gtsam.noiseModel.Isotropic.Sigma(6, 1.0)
    measurement = PoseMeasurement(0, i4x4, i3x3, i3x3)
    e = PriorPose(v, measurement, noise_model)
    element = GraphElement(edge=e)

    with pytest.raises(ValidationError):
        graph.add_element(element)


def test_add_element_with_incorrect_new_vertices_2():
    graph = Graph()
    t1, t2 = 0, 1
    noise_model = gtsam.noiseModel.Isotropic.Sigma(6, 1.0)
    measurement1 = PoseMeasurement(t1, i4x4, i3x3, i3x3)
    measurement2 = OdometryMeasurement(t2, TimeRange(t1, t2), i4x4, i3x3, i3x3)
    v1, v2 = PoseVertex(0), PoseVertex(1)
    cluster1, cluster2 = VertexCluster(), VertexCluster()

    e1 = PriorPose(v1, measurement1, noise_model)
    e2 = PoseOdometry(v1, v2, measurement2, noise_model)
    element1 = GraphElement(edge=e1, new_vertices=[NewVertex(v1, cluster1, t1)])
    element2 = GraphElement(
        edge=e2, new_vertices=[NewVertex(v1, cluster1, t1), NewVertex(v2, cluster2, t2)]
    )

    graph.add_element(element1)

    with pytest.raises(ValidationError):
        graph.add_element(element2)
