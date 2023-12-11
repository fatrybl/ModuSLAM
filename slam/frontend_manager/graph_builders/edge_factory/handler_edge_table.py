"""
Matches measurement handlers with edges
"""
from slam.frontend_manager.graph.edges import LidarOdometry
from slam.frontend_manager.handlers.pointcloid_registration.pointcloud_matcher import PointcloudMatcher

handler_edge_table = {
    PointcloudMatcher: LidarOdometry
}
