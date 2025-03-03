import pytest
from gtsam.noiseModel import Isotropic

from src.measurement_storage.measurements.pose import Pose as PoseMeasurement
from src.measurement_storage.measurements.pose_odometry import Odometry
from src.moduslam.frontend_manager.main_graph.data_classes import (
    GraphElement,
    NewVertex,
)
from src.moduslam.frontend_manager.main_graph.edges.pose import Pose as PriorPose
from src.moduslam.frontend_manager.main_graph.edges.pose_odometry import PoseOdometry
from src.moduslam.frontend_manager.main_graph.graph import Graph
from src.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from src.moduslam.frontend_manager.main_graph.vertices.custom import Pose as PoseVertex
from src.utils.auxiliary_dataclasses import TimeRange
from src.utils.auxiliary_objects import identity3x3 as i3x3
from src.utils.auxiliary_objects import identity4x4 as i4x4
from src.utils.exceptions import ValidationError
from src.utils.ordered_set import OrderedSet


def test_empty_graph():
    graph = Graph()
    v = PoseVertex(0)

    with pytest.raises(ValidationError):
        graph.remove_vertex(v)


def test_with_1_edge(noise: Isotropic):
    t = 0
    graph = Graph()
    v = PoseVertex(t)
    cluster = VertexCluster()
    measurement = PoseMeasurement(0, i4x4, i3x3, i3x3)
    e = PriorPose(v, measurement, noise)
    element = GraphElement(e, {v: t}, (NewVertex(v, cluster, t),))

    graph.add_element(element)

    graph.remove_vertex(v)

    assert e not in graph.edges
    assert v not in graph.connections
    assert v not in graph.vertex_storage
    assert graph.edges == OrderedSet()
    assert graph.factor_graph.nrFactors() == 0


def test_with_multiple_edges(noise: Isotropic):
    t1, t2, t3 = 0, 1, 2
    graph = Graph()
    v1, v2, v3 = PoseVertex(0), PoseVertex(1), PoseVertex(2)
    cluster1, cluster2, cluster3 = VertexCluster(), VertexCluster(), VertexCluster()
    measurement1 = Odometry(t2, TimeRange(t1, t2), i4x4, i3x3, i3x3)
    measurement2 = Odometry(t3, TimeRange(t1, t3), i4x4, i3x3, i3x3)
    e1 = PoseOdometry(v1, v2, measurement1, noise)
    e2 = PoseOdometry(v1, v3, measurement2, noise)
    element1 = GraphElement(
        e1, {v1: t1, v2: t2}, (NewVertex(v1, cluster1, t1), NewVertex(v2, cluster2, t2))
    )
    element2 = GraphElement(e2, {v1: t1, v3: t3}, (NewVertex(v3, cluster3, t3),))

    graph.add_element(element1)
    graph.add_element(element2)

    graph.remove_vertex(v1)

    edges = graph.edges
    connections = graph.connections
    storage = graph.vertex_storage

    assert e1 not in edges and e2 not in edges
    assert v1 not in storage and v2 not in storage and v3 not in storage
    assert v1 not in connections and v2 not in connections and v3 not in connections
    assert graph.edges == OrderedSet()
    assert graph.factor_graph.nrFactors() == 0


def test_in_cycle(noise: Isotropic):
    t1, t2, t3 = 0, 1, 2
    graph = Graph()
    v1, v2, v3 = PoseVertex(t1), PoseVertex(t2), PoseVertex(t3)
    cluster1, cluster2, cluster3 = VertexCluster(), VertexCluster(), VertexCluster()
    measurement1 = Odometry(t2, TimeRange(t1, t2), i4x4, i3x3, i3x3)
    measurement2 = Odometry(t3, TimeRange(t2, t3), i4x4, i3x3, i3x3)
    measurement3 = Odometry(t3, TimeRange(t1, t3), i4x4, i3x3, i3x3)
    e1 = PoseOdometry(v1, v2, measurement1, noise)
    e2 = PoseOdometry(v2, v3, measurement2, noise)
    e3 = PoseOdometry(v1, v3, measurement3, noise)
    element1 = GraphElement(
        e1, {v1: t1, v2: t2}, (NewVertex(v1, cluster1, t1), NewVertex(v2, cluster2, t2))
    )
    element2 = GraphElement(e2, {v2: t2, v3: t3}, (NewVertex(v3, cluster3, t3),))
    element3 = GraphElement(e3, {v1: t1, v3: t3}, ())
    o_set = OrderedSet[PoseOdometry]()
    o_set.add(e2)

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
    assert graph.edges == o_set
    assert graph.factor_graph.nrFactors() == 1
