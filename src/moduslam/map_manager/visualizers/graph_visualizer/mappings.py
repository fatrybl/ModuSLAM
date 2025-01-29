from src.moduslam.frontend_manager.main_graph.edges.base import Edge
from src.moduslam.frontend_manager.main_graph.edges.combined_imu_odometry import (
    ImuOdometry,
)
from src.moduslam.frontend_manager.main_graph.edges.gps_position import GpsPosition
from src.moduslam.frontend_manager.main_graph.edges.pose import Pose as PriorPose
from src.moduslam.frontend_manager.main_graph.edges.pose_odometry import PoseOdometry
from src.moduslam.frontend_manager.main_graph.vertices.base import Vertex
from src.moduslam.frontend_manager.main_graph.vertices.custom import (
    ImuBias,
    LinearVelocity,
    Pose,
)

vertex_types = {Pose, LinearVelocity, ImuBias}
edge_types = {GpsPosition, PoseOdometry, ImuOdometry}

vertex_encodings: dict[type[Vertex], str] = {
    Pose: "P",
    LinearVelocity: "V",
    ImuBias: "B",
}

edge_encodings: dict[type[Edge], str] = {
    GpsPosition: "GPS",
    PoseOdometry: "PoseOdom",
    ImuOdometry: "ImuOdom",
    PriorPose: "PriorPose",
}
