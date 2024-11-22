from typing import cast

import pytest

from moduslam.frontend_manager.noise_models import pose_diagonal_noise_model
from phd.bridge.edge_factories.split_pose_odometry import (
    Factory as SplitOdometryFactory,
)
from phd.bridge.objects.auxiliary_classes import SplitPoseOdometry
from phd.bridge.objects.measurements_cluster import Cluster
from phd.measurements.processed_measurements import Pose as PoseMeasurement
from phd.measurements.processed_measurements import PoseOdometry
from phd.moduslam.frontend_manager.main_graph.edges.pose import Pose as PriorPose
from phd.moduslam.frontend_manager.main_graph.graph import Graph, GraphElement
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.frontend_manager.main_graph.vertices.custom import Pose
from phd.moduslam.utils.auxiliary_dataclasses import TimeRange
from phd.moduslam.utils.auxiliary_objects import identity3x3, identity4x4
from phd.moduslam.utils.exceptions import SkipItemException


@pytest.fixture
def graph():
    graph = Graph()
    t1 = 0
    v1 = Pose(index=0)
    noise = pose_diagonal_noise_model((1, 1, 1, 1, 1, 1))
    m1 = PoseMeasurement(t1, identity4x4, identity3x3, identity3x3, [])
    edge1 = PriorPose(v1, m1, noise)
    new_vertices1 = {VertexCluster(): [(v1, t1)]}
    element1 = GraphElement(edge1, new_vertices1)
    graph.add_element(element1)
    return graph


def test_2_vertices_2_clusters(graph):
    """2 clusters with edges arrange by the creation order:
    1) [x0, x1]: prior, odom(x0-x2), odom(x1-x3)
    2) [x2, x3]: odom(x0-x2), odom(x1-x3)
    """
    measurement1 = PoseOdometry(2, TimeRange(0, 2), identity4x4, identity3x3, identity3x3, [])
    measurement2 = PoseOdometry(3, TimeRange(1, 3), identity4x4, identity3x3, identity3x3, [])

    split_odom_1_1 = SplitPoseOdometry(0, measurement1)
    split_odom_2_1 = SplitPoseOdometry(1, measurement2)
    split_odom_1_2 = SplitPoseOdometry(2, measurement1)
    split_odom_2_2 = SplitPoseOdometry(3, measurement2)

    m_cluster1, m_cluster2 = Cluster(), Cluster()
    m_cluster1.add(split_odom_1_1)
    m_cluster1.add(split_odom_2_1)
    m_cluster2.add(split_odom_1_2)
    m_cluster2.add(split_odom_2_2)

    clusters = {}

    for m_cluster in [m_cluster1, m_cluster2]:
        clusters.update({VertexCluster(): m_cluster.time_range})

        for m in m_cluster.measurements:
            split = cast(SplitPoseOdometry, m)
            try:
                new_element = SplitOdometryFactory.create(graph, clusters, split)
            except SkipItemException:
                continue

            graph.add_element(new_element)

    vertices = graph.vertex_storage.vertices
    (
        x0,
        x1,
    ) = (
        vertices[0],
        vertices[1],
    )

    assert len(graph.get_connected_edges(x0)) == 3
    assert len(graph.get_connected_edges(x1)) == 2

    assert graph.factor_graph.size() == 3
    assert graph.factor_graph.nrFactors() == 3
    assert len(graph.factor_graph.keyVector()) == 2

    assert len(graph.vertex_storage.vertices) == 2
    assert len(graph.edge_storage.edges) == 3
    assert len(graph.vertex_storage.clusters) == 2
    assert len(graph.connections) == 2


def test_4_vertices_4_clusters(graph):
    """4 clusters with edges arrange by the creation order:
    1) [x0]: prior, odom(x0-x2)
    2) [x1]: odom(x1-x3)
    3) [x2]: odom(x0-x2)
    4) [x3]: odom(x1-x3)
    """
    measurement1 = PoseOdometry(2, TimeRange(0, 2), identity4x4, identity3x3, identity3x3, [])
    measurement2 = PoseOdometry(3, TimeRange(1, 3), identity4x4, identity3x3, identity3x3, [])

    split_odom_1_1 = SplitPoseOdometry(0, measurement1)
    split_odom_2_1 = SplitPoseOdometry(1, measurement2)
    split_odom_1_2 = SplitPoseOdometry(2, measurement1)
    split_odom_2_2 = SplitPoseOdometry(3, measurement2)

    m_cluster1, m_cluster2, m_cluster3, m_cluster4 = Cluster(), Cluster(), Cluster(), Cluster()
    m_cluster1.add(split_odom_1_1)
    m_cluster2.add(split_odom_2_1)
    m_cluster3.add(split_odom_1_2)
    m_cluster4.add(split_odom_2_2)

    clusters = {}

    for m_cluster in [m_cluster1, m_cluster2, m_cluster3, m_cluster4]:
        clusters.update({VertexCluster(): m_cluster.time_range})

        for m in m_cluster.measurements:
            split = cast(SplitPoseOdometry, m)
            try:
                new_element = SplitOdometryFactory.create(graph, clusters, split)
            except SkipItemException:
                continue

            graph.add_element(new_element)

    vertices = graph.vertex_storage.vertices
    x0, x1, x2, x3 = vertices[0], vertices[1], vertices[2], vertices[3]

    assert len(graph.get_connected_edges(x0)) == 2
    assert len(graph.get_connected_edges(x1)) == 1
    assert len(graph.get_connected_edges(x2)) == 1
    assert len(graph.get_connected_edges(x3)) == 1

    assert len(graph.vertex_storage.vertices) == 4
    assert len(graph.edge_storage.edges) == 3
    assert len(graph.vertex_storage.clusters) == 4
    assert len(graph.connections) == 4

    assert graph.factor_graph.size() == 3
    assert graph.factor_graph.nrFactors() == 3
    assert len(graph.factor_graph.keyVector()) == 4


def test_3_vertices_3_clusters_common_mid(graph):
    """3 clusters with edges arranged by the creation order:
    1) [x0]: prior, odom(x0-x2)
    2) [x1, x2]: odom(x0-x2), odom(x1-x3)
    3) [x3]: odom(x1-x3)
    """
    measurement1 = PoseOdometry(2, TimeRange(0, 2), identity4x4, identity3x3, identity3x3, [])
    measurement2 = PoseOdometry(3, TimeRange(1, 3), identity4x4, identity3x3, identity3x3, [])

    split_odom_1_1 = SplitPoseOdometry(0, measurement1)
    split_odom_2_1 = SplitPoseOdometry(1, measurement2)
    split_odom_1_2 = SplitPoseOdometry(2, measurement1)
    split_odom_2_2 = SplitPoseOdometry(3, measurement2)

    m_cluster1, m_cluster2, m_cluster3 = Cluster(), Cluster(), Cluster()
    m_cluster1.add(split_odom_1_1)
    m_cluster2.add(split_odom_2_1)
    m_cluster2.add(split_odom_1_2)
    m_cluster3.add(split_odom_2_2)

    clusters = {}

    for m_cluster in [m_cluster1, m_cluster2, m_cluster3]:
        clusters.update({VertexCluster(): m_cluster.time_range})

        for m in m_cluster.measurements:
            split = cast(SplitPoseOdometry, m)
            try:
                new_element = SplitOdometryFactory.create(graph, clusters, split)
            except SkipItemException:
                continue

            graph.add_element(new_element)

    vertices = graph.vertex_storage.vertices
    x0, x1, x2 = vertices[0], vertices[1], vertices[2]

    assert len(graph.get_connected_edges(x0)) == 2
    assert len(graph.get_connected_edges(x1)) == 2
    assert len(graph.get_connected_edges(x2)) == 1

    assert len(graph.vertex_storage.vertices) == 3
    assert len(graph.edge_storage.edges) == 3
    assert len(graph.vertex_storage.clusters) == 3
    assert len(graph.connections) == 3

    assert graph.factor_graph.size() == 3
    assert graph.factor_graph.nrFactors() == 3
    assert len(graph.factor_graph.keyVector()) == 3


def test_3_vertices_3_clusters_common_left(graph):
    """3 clusters with edges arranged by the creation order:
    1) [x0, x1]: prior, odom(x0-x2), odom(x1-x3)
    2) [x2]: odom(x0-x2)
    3) [x3]: odom(x1-x3)
    """
    measurement1 = PoseOdometry(2, TimeRange(0, 2), identity4x4, identity3x3, identity3x3, [])
    measurement2 = PoseOdometry(3, TimeRange(1, 3), identity4x4, identity3x3, identity3x3, [])

    split_odom_1_1 = SplitPoseOdometry(0, measurement1)
    split_odom_2_1 = SplitPoseOdometry(1, measurement2)
    split_odom_1_2 = SplitPoseOdometry(2, measurement1)
    split_odom_2_2 = SplitPoseOdometry(3, measurement2)

    m_cluster1, m_cluster2, m_cluster3 = Cluster(), Cluster(), Cluster()
    m_cluster1.add(split_odom_1_1)
    m_cluster1.add(split_odom_2_1)
    m_cluster2.add(split_odom_1_2)
    m_cluster3.add(split_odom_2_2)

    clusters = {}

    for m_cluster in [m_cluster1, m_cluster2, m_cluster3]:
        clusters.update({VertexCluster(): m_cluster.time_range})

        for m in m_cluster.measurements:
            split = cast(SplitPoseOdometry, m)
            try:
                new_element = SplitOdometryFactory.create(graph, clusters, split)
            except SkipItemException:
                continue

            graph.add_element(new_element)

    vertices = graph.vertex_storage.vertices
    x0, x1, x2 = vertices[0], vertices[1], vertices[2]

    assert len(graph.get_connected_edges(x0)) == 3
    assert len(graph.get_connected_edges(x1)) == 1
    assert len(graph.get_connected_edges(x2)) == 1

    assert len(graph.vertex_storage.vertices) == 3
    assert len(graph.edge_storage.edges) == 3
    assert len(graph.vertex_storage.clusters) == 3
    assert len(graph.connections) == 3

    assert graph.factor_graph.size() == 3
    assert graph.factor_graph.nrFactors() == 3
    assert len(graph.factor_graph.keyVector()) == 3


def test_3_vertices_3_clusters_common_right(graph):
    """3 clusters with edges arranged by the creation order:
    1) [x0]: prior, odom(x0-x1),
    2) [x2]: odom(x2-x3)
    3) [x1, x3]: odom(x0-x1), odom(x2-x3)
    """
    measurement1 = PoseOdometry(2, TimeRange(0, 2), identity4x4, identity3x3, identity3x3, [])
    measurement2 = PoseOdometry(3, TimeRange(1, 3), identity4x4, identity3x3, identity3x3, [])

    split_odom_1_1 = SplitPoseOdometry(0, measurement1)
    split_odom_2_1 = SplitPoseOdometry(1, measurement2)
    split_odom_1_2 = SplitPoseOdometry(2, measurement1)
    split_odom_2_2 = SplitPoseOdometry(3, measurement2)

    m_cluster1, m_cluster2, m_cluster3 = Cluster(), Cluster(), Cluster()
    m_cluster1.add(split_odom_1_1)
    m_cluster2.add(split_odom_2_1)
    m_cluster3.add(split_odom_1_2)
    m_cluster3.add(split_odom_2_2)

    clusters = {}

    for m_cluster in [m_cluster1, m_cluster2, m_cluster3]:
        clusters.update({VertexCluster(): m_cluster.time_range})

        for m in m_cluster.measurements:
            split = cast(SplitPoseOdometry, m)
            try:
                new_element = SplitOdometryFactory.create(graph, clusters, split)
            except SkipItemException:
                continue

            graph.add_element(new_element)

    vertices = graph.vertex_storage.vertices
    x0, x1, x2 = vertices[0], vertices[1], vertices[2]

    assert len(graph.get_connected_edges(x0)) == 2
    assert len(graph.get_connected_edges(x1)) == 2
    assert len(graph.get_connected_edges(x2)) == 1

    assert len(graph.vertex_storage.vertices) == 3
    assert len(graph.edge_storage.edges) == 3
    assert len(graph.vertex_storage.clusters) == 3
    assert len(graph.connections) == 3

    assert graph.factor_graph.size() == 3
    assert graph.factor_graph.nrFactors() == 3
    assert len(graph.factor_graph.keyVector()) == 3
