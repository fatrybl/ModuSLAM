from moduslam.frontend_manager.main_graph.edges.base import Edge
from moduslam.frontend_manager.main_graph.edges.combined_imu_odometry import (
    ImuOdometry,
)
from moduslam.frontend_manager.main_graph.edges.gps_position import GpsPosition
from moduslam.frontend_manager.main_graph.edges.linear_velocity import (
    LinearVelocity as PriorVelocity,
)
from moduslam.frontend_manager.main_graph.edges.pose import Pose as PriorPose
from moduslam.frontend_manager.main_graph.edges.pose_odometry import PoseOdometry
from moduslam.frontend_manager.main_graph.vertices.base import Vertex
from moduslam.frontend_manager.main_graph.vertices.custom import (
    ImuBias,
    LinearVelocity,
    Pose,
)

vertex_types = {Pose, LinearVelocity, ImuBias}
edge_types = {GpsPosition, PoseOdometry, ImuOdometry}

vertex_encodings: dict[type[Vertex], str] = {
    Pose: "X",
    LinearVelocity: "V",
    ImuBias: "B",
}

edge_encodings: dict[type[Edge], str] = {
    GpsPosition: "GPS",
    PoseOdometry: "Lidar odom",
    ImuOdometry: "IMU odom",
    PriorPose: "Prior pose",
    PriorVelocity: "Prior velocity",
}
