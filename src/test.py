# from src.measurement_storage.measurements.imu import (
#     ContinuousImu,
#     ImuCovariance,
#     ImuData,
#     ProcessedImu,
# )
# from src.measurement_storage.measurements.pose import Pose as PoseMeasurement
# from src.moduslam.frontend_manager.main_graph.edges.imu_odometry import ImuOdometry
# from src.moduslam.frontend_manager.main_graph.edges.pose import Pose as PriorPose
# from src.moduslam.frontend_manager.main_graph.graph import Graph
# from src.moduslam.frontend_manager.main_graph.new_element import GraphElement, NewVertex
# from src.moduslam.frontend_manager.main_graph.vertex_storage.cluster import VertexCluster
# from src.moduslam.frontend_manager.main_graph.vertices.custom import (
#     ImuBias as BiasVertex,
#     LinearVelocity as VelocityVertex,
#     Pose as PoseVertex,
# )
# from src.moduslam.utils.auxiliary_objects import identity3x3, identity4x4, zero_vector3
#
# graph = Graph()
#
# noise = gtsam.noiseModel.Isotropic.Sigma(6, 1)
# preint_params = gtsam.gtsam.PreintegrationParams([9.81])
#
# data = ImuData(zero_vector3, zero_vector3)
# cov = ImuCovariance(identity3x3, identity3x3, identity3x3, identity3x3, identity3x3)
# imu1 = ProcessedImu(1, data, cov, identity4x4)
# imu2 = ProcessedImu(2, data, cov, identity4x4)
# continuous = ContinuousImu[ProcessedImu]([imu1, imu2], start=0, stop=3)
#
# pose1 = PoseMeasurement(0, identity4x4, identity3x3, identity3x3)
# pose2 = PoseMeasurement(3, identity4x4, identity3x3, identity3x3)
#
# p1, p2 = PoseVertex(0), PoseVertex(1)
# v1, v2 = VelocityVertex(0), VelocityVertex(1)
# b1, b2 = BiasVertex(0), BiasVertex(1)
# cluster1, cluster2 = VertexCluster(), VertexCluster()
#
# prior1 = PriorPose(p1, pose1, noise)
#
# pim = gtsam.PreintegratedImuMeasurements(preint_params, b1.backend_instance)
# imu_odom = ImuOdometry(p1, v1, b1, p2, v2, continuous, pim)
#
# new_element = GraphElement(
#     imu_odom,
#     new_vertices=[
#         NewVertex(p1, cluster1, 0),
#         NewVertex(v1, cluster1, 0),
#         NewVertex(b1, cluster1, 0),
#         NewVertex(p2, cluster2, 3),
#         NewVertex(v2, cluster2, 3),
#     ],
# )
# graph.add_element(new_element)
#
# cp = deepcopy(graph)
