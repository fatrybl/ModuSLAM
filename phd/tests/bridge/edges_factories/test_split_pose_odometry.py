import pytest

from phd.bridge.edge_factories.split_pose_odometry import Factory
from phd.bridge.objects.auxiliary_classes import SplitPoseOdometry
from phd.measurements.processed_measurements import PoseOdometry
from phd.moduslam.frontend_manager.main_graph.graph import Graph
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.frontend_manager.main_graph.vertices.custom import Pose
from phd.moduslam.utils.auxiliary_dataclasses import TimeRange
from phd.moduslam.utils.auxiliary_objects import identity3x3, identity4x4
from phd.moduslam.utils.exceptions import SkipItemException


def test_create_empty_graph_1_split(empty_graph: Graph):
    parent = PoseOdometry(1, TimeRange(0, 1), identity4x4, identity3x3, identity3x3, [])
    measurement = SplitPoseOdometry(0, parent)
    cluster = VertexCluster()
    clusters = {cluster: TimeRange(0, 0)}

    with pytest.raises(SkipItemException):
        Factory.create(empty_graph, clusters, measurement)


def test_create_empty_graph_2_splits(empty_graph: Graph):
    parent = PoseOdometry(1, TimeRange(0, 1), identity4x4, identity3x3, identity3x3, [])
    split1 = SplitPoseOdometry(0, parent)
    split2 = SplitPoseOdometry(1, parent)
    cluster1, cluster2 = VertexCluster(), VertexCluster()
    clusters = {cluster1: TimeRange(0, 0), cluster2: TimeRange(1, 1)}
    measurements = [split1, split2]

    with pytest.raises(SkipItemException):
        Factory.create(empty_graph, clusters, measurements[0])

    new_element = Factory.create(empty_graph, clusters, measurements[1])

    edge_vertex1 = new_element.edge.vertex1
    edge_vertex2 = new_element.edge.vertex2
    new_vertex1 = new_element.new_vertices[0]
    new_vertex2 = new_element.new_vertices[1]

    assert len(new_element.new_vertices) == 2
    assert edge_vertex1.index == 0
    assert edge_vertex2.index == 1
    assert edge_vertex1 is new_vertex1.instance
    assert edge_vertex2 is new_vertex2.instance
    assert new_vertex1.timestamp == 0
    assert new_vertex2.timestamp == 1


def test_create_graph_1_split(graph1: Graph):
    parent = PoseOdometry(1, TimeRange(0, 1), identity4x4, identity3x3, identity3x3, [])
    measurement = SplitPoseOdometry(0, parent)
    cluster = VertexCluster()
    clusters = {cluster: TimeRange(0, 0)}

    with pytest.raises(SkipItemException):
        Factory.create(graph1, clusters, measurement)

    pose_in_cluster = cluster.get_last_vertex(Pose)
    pose_in_graph = graph1.vertex_storage.get_last_vertex(Pose)

    assert pose_in_cluster is pose_in_graph


def test_create_graph_2_splits(graph1: Graph):
    parent = PoseOdometry(1, TimeRange(0, 1), identity4x4, identity3x3, identity3x3, [])
    split1 = SplitPoseOdometry(0, parent)
    split2 = SplitPoseOdometry(1, parent)
    cluster1, cluster2 = VertexCluster(), VertexCluster()
    clusters = {cluster1: TimeRange(0, 0), cluster2: TimeRange(1, 1)}
    measurements = [split1, split2]

    with pytest.raises(SkipItemException):
        Factory.create(graph1, clusters, measurements[0])

    pose_in_cluster = cluster1.get_last_vertex(Pose)
    pose_in_graph = graph1.vertex_storage.get_last_vertex(Pose)

    assert pose_in_cluster is pose_in_graph

    new_element = Factory.create(graph1, clusters, measurements[1])

    edge_vertex1 = new_element.edge.vertex1
    edge_vertex2 = new_element.edge.vertex2
    t = new_element.new_vertices[0].timestamp

    assert len(new_element.new_vertices) == 1
    assert edge_vertex1.index == 0
    assert edge_vertex2.index == 1
    assert edge_vertex1 is pose_in_graph
    assert t == 1


def test_create_graph_with_2_vertices_2_splits(graph2: Graph):
    parent = PoseOdometry(1, TimeRange(0, 1), identity4x4, identity3x3, identity3x3, [])
    split1 = SplitPoseOdometry(0, parent)
    split2 = SplitPoseOdometry(1, parent)
    cluster1, cluster2 = VertexCluster(), VertexCluster()
    clusters = {cluster1: TimeRange(0, 0), cluster2: TimeRange(1, 1)}
    measurements = [split1, split2]

    with pytest.raises(SkipItemException):
        Factory.create(graph2, clusters, measurements[0])

    pose_in_cluster = cluster1.get_last_vertex(Pose)
    pose1_in_graph = graph2.vertex_storage.vertices[0]
    pose2_in_graph = graph2.vertex_storage.vertices[1]

    assert pose_in_cluster is pose1_in_graph

    new_element = Factory.create(graph2, clusters, measurements[1])

    edge_vertex1 = new_element.edge.vertex1
    edge_vertex2 = new_element.edge.vertex2

    assert len(new_element.new_vertices) == 0
    assert edge_vertex1.index == 0
    assert edge_vertex2.index == 1
    assert edge_vertex1 is pose1_in_graph
    assert edge_vertex2 is pose2_in_graph
