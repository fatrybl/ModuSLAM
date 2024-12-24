import gtsam
import pytest

from phd.measurement_storage.measurements.pose import Pose as PoseMeasurement
from phd.measurement_storage.measurements.pose_odometry import Odometry
from phd.moduslam.frontend_manager.main_graph.edges.pose import Pose as PriorPose
from phd.moduslam.frontend_manager.main_graph.edges.pose_odometry import PoseOdometry
from phd.moduslam.frontend_manager.main_graph.graph import Graph
from phd.moduslam.frontend_manager.main_graph.new_element import GraphElement, NewVertex
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.frontend_manager.main_graph.vertices.custom import Pose as PoseVertex
from phd.utils.auxiliary_dataclasses import TimeRange
from phd.utils.auxiliary_objects import identity3x3 as i3x3
from phd.utils.auxiliary_objects import identity4x4 as i4x4
from phd.utils.exceptions import ValidationError


def test_remove_vertex_empty_graph():
    graph = Graph()
    v = PoseVertex(0)

    with pytest.raises(ValidationError):
        graph.remove_vertex(v)


def test_remove_vertex_with_1_edge():
    t = 0
    graph = Graph()
    v = PoseVertex(t)
    cluster = VertexCluster()
    noise_model = gtsam.noiseModel.Isotropic.Sigma(6, 1.0)
    measurement = PoseMeasurement(0, i4x4, i3x3, i3x3)
    e = PriorPose(v, measurement, noise_model)
    element = GraphElement(e, new_vertices=[NewVertex(v, cluster, t)])

    graph.add_element(element)

    graph.remove_vertex(v)

    assert e not in graph.edges
    assert v not in graph.connections
    assert v not in graph.vertex_storage
    assert len(graph.edges) == 0
    assert graph.factor_graph.nrFactors() == 0


def test_remove_vertex_with_multiple_edges():
    t1, t2, t3 = 0, 1, 2
    graph = Graph()
    v1, v2, v3 = PoseVertex(0), PoseVertex(1), PoseVertex(2)
    cluster1, cluster2, cluster3 = VertexCluster(), VertexCluster(), VertexCluster()
    noise_model = gtsam.noiseModel.Isotropic.Sigma(6, 1.0)

    measurement1 = Odometry(t2, TimeRange(t1, t2), i4x4, i3x3, i3x3)
    measurement2 = Odometry(t3, TimeRange(t1, t3), i4x4, i3x3, i3x3)

    e1 = PoseOdometry(v1, v2, measurement1, noise_model)
    e2 = PoseOdometry(v1, v3, measurement2, noise_model)

    element1 = GraphElement(
        e1, new_vertices=[NewVertex(v1, cluster1, t1), NewVertex(v2, cluster2, t2)]
    )
    element2 = GraphElement(e2, new_vertices=[NewVertex(v3, cluster3, t3)])

    graph.add_element(element1)
    graph.add_element(element2)

    graph.remove_vertex(v1)

    edges = graph.edges
    connections = graph.connections
    storage = graph.vertex_storage

    assert e1 not in edges and e2 not in edges
    assert v1 not in storage and v2 not in storage and v3 not in storage
    assert v1 not in connections and v2 not in connections and v3 not in connections
    assert len(graph.edges) == 0
    assert graph.factor_graph.nrFactors() == 0


def test_remove_vertex_in_cycle():
    t1, t2, t3 = 0, 1, 2
    graph = Graph()
    v1, v2, v3 = PoseVertex(t1), PoseVertex(t2), PoseVertex(t3)
    cluster1, cluster2, cluster3 = VertexCluster(), VertexCluster(), VertexCluster()
    noise_model = gtsam.noiseModel.Isotropic.Sigma(6, 1.0)

    measurement1 = Odometry(t2, TimeRange(t1, t2), i4x4, i3x3, i3x3)
    measurement2 = Odometry(t3, TimeRange(t2, t3), i4x4, i3x3, i3x3)
    measurement3 = Odometry(t3, TimeRange(t1, t3), i4x4, i3x3, i3x3)

    e1 = PoseOdometry(v1, v2, measurement1, noise_model)
    e2 = PoseOdometry(v2, v3, measurement2, noise_model)
    e3 = PoseOdometry(v1, v3, measurement3, noise_model)

    element1 = GraphElement(
        e1, new_vertices=[NewVertex(v1, cluster1, t1), NewVertex(v2, cluster2, t2)]
    )
    element2 = GraphElement(e2, new_vertices=[NewVertex(v3, cluster3, t3)])
    element3 = GraphElement(e3, new_vertices=[])

    graph.add_element(element1)
    graph.add_element(element2)
    graph.add_element(element3)

    graph.remove_vertex(v1)

    edges = graph.edges
    connections = graph.connections
    storage = graph.vertex_storage

    assert e1 not in edges and e3 not in edges
    assert e2 in edges
    assert v1 not in storage
    assert v2 in storage and v3 in storage
    assert v1 not in connections
    assert v2 in connections and v3 in connections
    assert len(graph.edges) == 1
    assert graph.factor_graph.nrFactors() == 1
