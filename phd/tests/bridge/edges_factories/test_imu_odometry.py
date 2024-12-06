import pytest

from phd.bridge.edge_factories.imu_odometry.odometry import Factory
from phd.measurements.processed import ContinuousImuMeasurement
from phd.measurements.processed import Imu as ImuMeasurement
from phd.measurements.processed import LinearVelocity as VelocityMeasurement
from phd.measurements.processed import Pose as PoseMeasurement
from phd.moduslam.data_manager.batch_factory.batch import Element, RawMeasurement
from phd.moduslam.data_manager.batch_factory.readers.locations import Location
from phd.moduslam.frontend_manager.handlers.imu_data_preprocessors.objects import (
    ImuCovariance,
    ImuData,
)
from phd.moduslam.frontend_manager.main_graph.edges.linear_velocity import (
    LinearVelocity as PriorVelocity,
)
from phd.moduslam.frontend_manager.main_graph.edges.noise_models import (
    diagonal3x3_noise_model,
    se3_isotropic_noise_model,
)
from phd.moduslam.frontend_manager.main_graph.edges.pose import Pose as PriorPose
from phd.moduslam.frontend_manager.main_graph.graph import Graph, GraphElement
from phd.moduslam.frontend_manager.main_graph.new_element import NewVertex
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.frontend_manager.main_graph.vertices.custom import (
    LinearVelocity,
    Pose,
)
from phd.moduslam.setup_manager.sensors_factory.sensors import Imu as ImuSensor
from phd.moduslam.setup_manager.sensors_factory.sensors_configs import ImuConfig
from phd.moduslam.utils.auxiliary_dataclasses import TimeRange
from phd.moduslam.utils.auxiliary_objects import (
    identity3x3,
    identity4x4,
    one_vector3,
    zero_vector3,
)


@pytest.fixture
def measurement() -> ContinuousImuMeasurement:
    tf = identity4x4
    measurement = RawMeasurement(ImuSensor(ImuConfig(name="imu")), None)
    el1 = Element(0, measurement, Location())
    el2 = Element(1, measurement, Location())
    el3 = Element(2, measurement, Location())
    data1 = ImuData(one_vector3, one_vector3)
    data2 = ImuData(one_vector3, one_vector3)
    data3 = ImuData(one_vector3, one_vector3)
    cov = ImuCovariance(identity3x3, identity3x3, identity3x3, identity3x3, identity3x3)
    imu1 = ImuMeasurement(el1, data1, cov, tf)
    imu2 = ImuMeasurement(el2, data2, cov, tf)
    imu3 = ImuMeasurement(el3, data3, cov, tf)
    return ContinuousImuMeasurement([imu1, imu2, imu3], start=0, stop=3)


@pytest.fixture
def graph_2_poses():
    graph = Graph()
    t1, t2 = 0, 3
    idx1, idx2 = 0, 1
    v1, v2 = Pose(index=idx1), Pose(index=idx2)
    noise = se3_isotropic_noise_model(1)
    m1 = PoseMeasurement(t1, identity4x4, identity3x3, identity3x3, [])
    m2 = PoseMeasurement(t2, identity4x4, identity3x3, identity3x3, [])
    edge1 = PriorPose(v1, m1, noise)
    edge2 = PriorPose(v2, m2, noise)
    cluster1, cluster2 = VertexCluster(), VertexCluster()
    element1 = GraphElement(edge1, [NewVertex(v1, cluster1, t1)])
    element2 = GraphElement(edge2, [NewVertex(v2, cluster2, t2)])
    graph.add_element(element1)
    graph.add_element(element2)
    return graph


@pytest.fixture
def graph_2_velocities():
    graph = Graph()
    t1, t2 = 0, 3
    idx1, idx2 = 0, 1
    v1, v2 = LinearVelocity(idx1), LinearVelocity(idx2)
    noise = diagonal3x3_noise_model((1, 1, 1))
    m1 = VelocityMeasurement(t1, zero_vector3, identity3x3, [])
    m2 = VelocityMeasurement(t2, zero_vector3, identity3x3, [])
    edge1 = PriorVelocity(v1, m1, noise)
    edge2 = PriorVelocity(v2, m2, noise)
    cluster1, cluster2 = VertexCluster(), VertexCluster()
    element1 = GraphElement(edge1, [NewVertex(v1, cluster1, t1)])
    element2 = GraphElement(edge2, [NewVertex(v2, cluster2, t2)])
    graph.add_element(element1)
    graph.add_element(element2)
    return graph


def test_create_empty_graph(empty_graph: Graph, measurement: ContinuousImuMeasurement):
    t = 3
    cluster = VertexCluster()
    clusters = {cluster: TimeRange(t, t)}

    new_element = Factory.create(empty_graph, clusters, measurement)

    edge = new_element.edge
    new_pose_j = new_element.new_vertices[3]
    cluster2 = new_pose_j.cluster

    assert cluster2 is cluster
    assert len(new_element.new_vertices) == len(edge.vertices) == 6
    assert edge.pose_i.index == 0
    assert edge.pose_i is not edge.pose_j
    assert edge.pose_j.index == 1
    assert edge.velocity_i.index == 0
    assert edge.velocity_i is not edge.velocity_j
    assert edge.velocity_j.index == 1
    assert edge.bias_i.index == 0
    assert edge.bias_i is not edge.bias_j
    assert edge.bias_j.index == 1


def test_create_graph_with_1_existing_pose(graph1: Graph, measurement: ContinuousImuMeasurement):
    t = 3
    cluster = VertexCluster()
    clusters = {cluster: TimeRange(t, t)}

    new_element = Factory.create(graph1, clusters, measurement)

    edge = new_element.edge
    new_pose_j = new_element.new_vertices[2]
    cluster2 = new_pose_j.cluster
    existing_pose = graph1.vertex_storage.vertices[0]

    assert cluster2 is cluster
    assert len(new_element.new_vertices) == 5
    assert len(edge.vertices) == 6
    assert new_pose_j.instance is not existing_pose
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


def test_create_graph_with_2_existing_poses(
    graph_2_poses: Graph, measurement: ContinuousImuMeasurement
):
    t = 3
    cluster = VertexCluster()
    clusters = {cluster: TimeRange(t, t)}

    new_element = Factory.create(graph_2_poses, clusters, measurement)

    edge = new_element.edge
    existing_pose_1 = graph_2_poses.vertex_storage.vertices[0]
    existing_pose_2 = graph_2_poses.vertex_storage.vertices[1]
    cluster1 = new_element.new_vertices[0].cluster
    cluster2 = new_element.new_vertices[2].cluster

    assert cluster1 is not cluster
    assert cluster2 is not cluster
    assert len(new_element.new_vertices) == 4
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


def test_create_graph_with_2_existing_velocities(
    graph_2_velocities: Graph, measurement: ContinuousImuMeasurement
):
    t = 3
    cluster = VertexCluster()
    clusters = {cluster: TimeRange(t, t)}

    new_element = Factory.create(graph_2_velocities, clusters, measurement)

    edge = new_element.edge
    existing_velocity_1 = graph_2_velocities.vertex_storage.vertices[0]
    existing_velocity_2 = graph_2_velocities.vertex_storage.vertices[1]
    cluster1 = new_element.new_vertices[0].cluster
    cluster2 = new_element.new_vertices[2].cluster

    assert cluster1 is not cluster
    assert cluster2 is not cluster
    assert len(new_element.new_vertices) == 4
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
