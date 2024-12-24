"""TODO: change tests."""

import pytest

from phd.measurement_storage.measurements.pose import Pose as PoseMeasurement
from phd.moduslam.frontend_manager.main_graph.edges.noise_models import (
    se3_isotropic_noise_model,
)
from phd.moduslam.frontend_manager.main_graph.edges.pose import Pose as PriorPose
from phd.moduslam.frontend_manager.main_graph.graph import Graph, GraphElement
from phd.moduslam.frontend_manager.main_graph.new_element import NewVertex
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.frontend_manager.main_graph.vertices.custom import Pose
from phd.moduslam.sensors_factory.configs import SensorConfig
from phd.moduslam.sensors_factory.factory import SensorsFactory
from phd.utils.auxiliary_objects import identity3x3 as i3x3
from phd.utils.auxiliary_objects import identity4x4 as i4x4


@pytest.fixture
def graph():
    graph = Graph()
    t1 = 0
    v1 = Pose(index=0)
    noise = se3_isotropic_noise_model(1)
    m1 = PoseMeasurement(t1, i4x4, i3x3, i3x3)
    edge1 = PriorPose(v1, m1, noise)
    cluster = VertexCluster()
    element1 = GraphElement(edge1, [NewVertex(v1, cluster, t1)])
    graph.add_element(element1)
    return graph


@pytest.fixture(autouse=True, scope="module")
def create_sensors():
    sensor_configs = {"imu": SensorConfig(name="imu")}
    SensorsFactory.init_sensors(sensor_configs)


# def test_2_vertices_2_clusters(graph, clean_storage):
#     """2 clusters with edges arrange by the creation order:
#     1) [x0, x1]: prior, odom(x0-x2), odom(x1-x3)
#     2) [x2, x3]: odom(x0-x2), odom(x1-x3)
#
#     TODO: add more checks.
#     """
#     storage = MeasurementStorage
#     data = ImuData(zero_vector3, zero_vector3)
#     covariance = ImuCovariance(i3x3, i3x3, i3x3, i3x3, i3x3)
#     odom1 = Odometry(4, TimeRange(0, 4), i4x4, i3x3, i3x3)
#     odom2 = Odometry(6, TimeRange(2, 6), i4x4, i3x3, i3x3)
#     imu1 = ProcessedImu(1, data, covariance, i4x4)
#     imu2 = ProcessedImu(2, data, covariance, i4x4)
#     imu3 = ProcessedImu(3, data, covariance, i4x4)
#     imu4 = ProcessedImu(4, data, covariance, i4x4)
#     imu5 = ProcessedImu(5, data, covariance, i4x4)
#     factory = CandidatesFactory()
#
#     storage.add(odom1)
#     storage.add(odom2)
#     for imu in [imu1, imu2, imu3, imu4, imu5]:
#         storage.add(imu)
#
#     storage_data = storage.data()
#     candidates = factory.create_candidates(graph, storage_data)
#
#     assert len(candidates) == 11
#
#
# def test_4_vertices_4_clusters(graph, clean_storage):
#     """4 clusters with edges arrange by the creation order:
#     1) [x0]: prior, odom(x0-x2)
#     2) [x1]: odom(x1-x3)
#     3) [x2]: odom(x0-x2)
#     4) [x3]: odom(x1-x3)
#     """
#     storage = MeasurementStorage
#     odom1 = Odometry(2, TimeRange(0, 2), i4x4, i3x3, i3x3)
#     odom2 = Odometry(3, TimeRange(1, 3), i4x4, i3x3, i3x3)
#     split_odom_1_1 = SplitPoseOdometry(0, odom1)
#     split_odom_2_1 = SplitPoseOdometry(1, odom2)
#     split_odom_1_2 = SplitPoseOdometry(2, odom1)
#     split_odom_2_2 = SplitPoseOdometry(3, odom2)
#     factory = CandidatesFactory()
#
#     for m in [split_odom_1_1, split_odom_2_1, split_odom_1_2, split_odom_2_2]:
#         storage.add(m)
#
#     storage_data = storage.data()
#     candidates = factory.create_candidates(graph, storage_data)
#
#     assert len(candidates) == 5
#
#
# def test_3_vertices_3_clusters_common_mid(graph, clean_storage):
#     """3 clusters with edges arranged by the creation order:
#     1) [x0]: prior, odom(x0-x2)
#     2) [x1, x2]: odom(x0-x2), odom(x1-x3)
#     3) [x3]: odom(x1-x3)
#     """
#     storage = MeasurementStorage
#     odom1 = Odometry(2, TimeRange(0, 2), i4x4, i3x3, i3x3)
#     odom2 = Odometry(3, TimeRange(1, 3), i4x4, i3x3, i3x3)
#     split_odom_1_1 = SplitPoseOdometry(0, odom1)
#     split_odom_2_1 = SplitPoseOdometry(1, odom2)
#     split_odom_1_2 = SplitPoseOdometry(2, odom1)
#     split_odom_2_2 = SplitPoseOdometry(3, odom2)
#     factory = CandidatesFactory()
#
#     for m in [split_odom_1_1, split_odom_2_1, split_odom_1_2, split_odom_2_2]:
#         storage.add(m)
#
#     storage_data = storage.data()
#     candidates = factory.create_candidates(graph, storage_data)
#
#     assert len(candidates) == 5
#
#
# def test_3_vertices_3_clusters_common_left(graph, clean_storage):
#     """3 clusters with edges arranged by the creation order:
#     1) [x0, x1]: prior, odom(x0-x2), odom(x1-x3)
#     2) [x2]: odom(x0-x2)
#     3) [x3]: odom(x1-x3)
#     """
#     storage = MeasurementStorage
#     odom1 = Odometry(2, TimeRange(0, 2), i4x4, i3x3, i3x3)
#     odom2 = Odometry(3, TimeRange(1, 3), i4x4, i3x3, i3x3)
#     split_odom_1_1 = SplitPoseOdometry(0, odom1)
#     split_odom_2_1 = SplitPoseOdometry(1, odom2)
#     split_odom_1_2 = SplitPoseOdometry(2, odom1)
#     split_odom_2_2 = SplitPoseOdometry(3, odom2)
#     factory = CandidatesFactory()
#
#     for m in [split_odom_1_1, split_odom_2_1, split_odom_1_2, split_odom_2_2]:
#         storage.add(m)
#
#     storage_data = storage.data()
#     candidates = factory.create_candidates(graph, storage_data)
#
#     assert len(candidates) == 5
#
#
# def test_3_vertices_3_clusters_common_right(graph, clean_storage):
#     """3 clusters with edges arranged by the creation order:
#     1) [x0]: prior, odom(x0-x1),
#     2) [x2]: odom(x2-x3)
#     3) [x1, x3]: odom(x0-x1), odom(x2-x3)
#     """
#     storage = MeasurementStorage
#     odom1 = Odometry(2, TimeRange(0, 2), i4x4, i3x3, i3x3)
#     odom2 = Odometry(3, TimeRange(1, 3), i4x4, i3x3, i3x3)
#     split_odom_1_1 = SplitPoseOdometry(0, odom1)
#     split_odom_2_1 = SplitPoseOdometry(1, odom2)
#     split_odom_1_2 = SplitPoseOdometry(2, odom1)
#     split_odom_2_2 = SplitPoseOdometry(3, odom2)
#     factory = CandidatesFactory()
#
#     for m in [split_odom_1_1, split_odom_2_1, split_odom_1_2, split_odom_2_2]:
#         storage.add(m)
#
#     storage_data = storage.data()
#     candidates = factory.create_candidates(graph, storage_data)
#
#     assert len(candidates) == 5
