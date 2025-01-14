import pytest

from src.bridge.edge_factories.imu_odometry.combined_odometry import Factory
from src.measurement_storage.measurements.imu import (
    ContinuousImu,
    ImuCovariance,
    ImuData,
    ProcessedImu,
)
from src.measurement_storage.measurements.linear_velocity import (
    Velocity as VelocityMeasurement,
)
from src.measurement_storage.measurements.pose import Pose as PoseMeasurement
from src.moduslam.frontend_manager.main_graph.data_classes import NewVertex
from src.moduslam.frontend_manager.main_graph.edges.linear_velocity import (
    LinearVelocity as PriorVelocity,
)
from src.moduslam.frontend_manager.main_graph.edges.noise_models import (
    isotropic_3d_noise_model,
    se3_isotropic_noise_model,
)
from src.moduslam.frontend_manager.main_graph.edges.pose import Pose as PriorPose
from src.moduslam.frontend_manager.main_graph.graph import Graph, GraphElement
from src.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from src.moduslam.frontend_manager.main_graph.vertices.custom import (
    LinearVelocity,
    Pose,
)
from src.utils.auxiliary_dataclasses import TimeRange
from src.utils.auxiliary_objects import identity3x3 as i3x3
from src.utils.auxiliary_objects import identity4x4 as i4x4
from src.utils.auxiliary_objects import one_vector3, zero_vector3


@pytest.fixture
def measurement() -> ContinuousImu[ProcessedImu]:
    """Continuous IMU measurement with 3 raw measurements"""
    t1, t2 = 0, 3
    data = ImuData(one_vector3, one_vector3)
    cov = ImuCovariance(i3x3, i3x3, i3x3, i3x3, i3x3)
    imu1 = ProcessedImu(0, data, cov, i4x4)
    imu2 = ProcessedImu(1, data, cov, i4x4)
    imu3 = ProcessedImu(2, data, cov, i4x4)
    return ContinuousImu([imu1, imu2, imu3], start=t1, stop=t2)


@pytest.fixture
def graph_2_poses():
    """Graph with 2 poses."""
    graph = Graph()
    t1, t2 = 0, 3
    idx1, idx2 = 0, 1
    v1, v2 = Pose(idx1), Pose(idx2)
    noise = se3_isotropic_noise_model(1)
    m1, m2 = PoseMeasurement(t1, i4x4, i3x3, i3x3), PoseMeasurement(t2, i4x4, i3x3, i3x3)
    edge1, edge2 = PriorPose(v1, m1, noise), PriorPose(v2, m2, noise)
    cluster1, cluster2 = VertexCluster(), VertexCluster()
    element1 = GraphElement(edge1, {v1: t1}, (NewVertex(v1, cluster1, t1),))
    element2 = GraphElement(edge2, {v2: t2}, (NewVertex(v2, cluster2, t2),))
    graph.add_element(element1)
    graph.add_element(element2)
    return graph


@pytest.fixture
def graph_2_velocities():
    """Graph with 2 velocities."""
    graph = Graph()
    noise = isotropic_3d_noise_model(1)
    t1, t2 = 0, 3
    idx1, idx2 = 0, 1
    v1, v2 = LinearVelocity(idx1), LinearVelocity(idx2)
    m1 = VelocityMeasurement(t1, zero_vector3, i3x3)
    m2 = VelocityMeasurement(t2, zero_vector3, i3x3)
    edge1, edge2 = PriorVelocity(v1, m1, noise), PriorVelocity(v2, m2, noise)
    cluster1, cluster2 = VertexCluster(), VertexCluster()
    element1 = GraphElement(edge1, {v1: t1}, (NewVertex(v1, cluster1, t1),))
    element2 = GraphElement(edge2, {v2: t2}, (NewVertex(v2, cluster2, t2),))
    graph.add_element(element1)
    graph.add_element(element2)
    return graph


def test_empty_graph(graph0: Graph, measurement: ContinuousImu):
    t1, t2 = 0, 3
    clusters = {VertexCluster(): TimeRange(t2, t2)}

    element = Factory.create(graph0, clusters, measurement)

    edge = element.edge

    assert len(element.new_vertices) == len(edge.vertices) == 6
    assert edge.pose_i.index == 0
    assert edge.pose_i is not edge.pose_j
    assert edge.pose_j.index == 1
    assert edge.velocity_i.index == 0
    assert edge.velocity_i is not edge.velocity_j
    assert edge.velocity_j.index == 1
    assert edge.bias_i.index == 0
    assert edge.bias_i is not edge.bias_j
    assert edge.bias_j.index == 1
    assert element.vertex_timestamp_table == {
        edge.pose_i: t1,
        edge.velocity_i: t1,
        edge.bias_i: t1,
        edge.pose_j: t2,
        edge.velocity_j: t2,
        edge.bias_j: t2,
    }


def test_create_graph_with_1_existing_pose(graph1: Graph, measurement: ContinuousImu[ProcessedImu]):
    t1, t2 = 0, 3
    clusters = {VertexCluster(): TimeRange(t2, t2)}
    existing_pose = graph1.vertex_storage.vertices[0]

    element = Factory.create(graph1, clusters, measurement)

    edge = element.edge

    assert len(element.new_vertices) == 5
    assert len(edge.vertices) == 6
    assert edge.pose_j is not existing_pose
    assert edge.pose_i is existing_pose
    assert edge.pose_i.index == 0
    assert edge.pose_i is not edge.pose_j
    assert edge.pose_j.index == 1
    assert edge.velocity_i.index == 0
    assert edge.velocity_i is not edge.velocity_j
    assert edge.velocity_j.index == 1
    assert edge.bias_i.index == 0
    assert edge.bias_i is not edge.bias_j
    assert edge.bias_j.index == 1
    assert element.vertex_timestamp_table == {
        edge.pose_i: t1,
        edge.velocity_i: t1,
        edge.bias_i: t1,
        edge.pose_j: t2,
        edge.velocity_j: t2,
        edge.bias_j: t2,
    }


def test_create_graph_with_2_existing_poses(
    graph_2_poses: Graph, measurement: ContinuousImu[ProcessedImu]
):
    t1, t2 = 0, 3
    cluster = VertexCluster()
    clusters = {VertexCluster(): TimeRange(t2, t2)}
    existing_pose_1 = graph_2_poses.vertex_storage.vertices[0]
    existing_pose_2 = graph_2_poses.vertex_storage.vertices[1]

    element = Factory.create(graph_2_poses, clusters, measurement)

    edge = element.edge
    assert len(element.new_vertices) == 4
    cluster1 = element.new_vertices[0].cluster
    cluster2 = element.new_vertices[2].cluster

    assert cluster1 is not cluster
    assert cluster2 is not cluster
    assert len(edge.vertices) == 6
    assert edge.pose_i is existing_pose_1
    assert edge.pose_i.index == 0
    assert edge.pose_i is not edge.pose_j
    assert edge.pose_j.index == 1
    assert edge.pose_j is existing_pose_2
    assert edge.velocity_i.index == 0
    assert edge.velocity_i is not edge.velocity_j
    assert edge.velocity_j.index == 1
    assert edge.bias_i.index == 0
    assert edge.bias_i is not edge.bias_j
    assert edge.bias_j.index == 1
    assert element.vertex_timestamp_table == {
        edge.pose_i: t1,
        edge.velocity_i: t1,
        edge.bias_i: t1,
        edge.pose_j: t2,
        edge.velocity_j: t2,
        edge.bias_j: t2,
    }


def test_create_graph_with_2_existing_velocities(
    graph_2_velocities: Graph, measurement: ContinuousImu[ProcessedImu]
):
    t1, t2 = 0, 3
    cluster = VertexCluster()
    clusters = {cluster: TimeRange(t2, t2)}
    existing_velocity_1 = graph_2_velocities.vertex_storage.vertices[0]
    existing_velocity_2 = graph_2_velocities.vertex_storage.vertices[1]

    element = Factory.create(graph_2_velocities, clusters, measurement)

    edge = element.edge

    assert len(element.new_vertices) == 4

    cluster1 = element.new_vertices[0].cluster
    cluster2 = element.new_vertices[2].cluster

    assert cluster1 is not cluster
    assert cluster2 is not cluster
    assert len(edge.vertices) == 6
    assert edge.pose_i.index == 0
    assert edge.pose_i is not edge.pose_j
    assert edge.pose_j.index == 1
    assert edge.velocity_i.index == 0
    assert edge.velocity_i is existing_velocity_1
    assert edge.velocity_i is not edge.velocity_j
    assert edge.velocity_j.index == 1
    assert edge.velocity_j is existing_velocity_2
    assert edge.bias_i.index == 0
    assert edge.bias_i is not edge.bias_j
    assert edge.bias_j.index == 1
    assert element.vertex_timestamp_table == {
        edge.pose_i: t1,
        edge.velocity_i: t1,
        edge.bias_i: t1,
        edge.pose_j: t2,
        edge.velocity_j: t2,
        edge.bias_j: t2,
    }
