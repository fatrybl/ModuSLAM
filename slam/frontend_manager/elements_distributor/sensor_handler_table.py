"""
A dictionary {<sensor_name>, <handler>} to distribute different sensors` raw measurements to corresponding handlers.
"""


from slam.frontend_manager.handlers.ABC_handler import ElementHandler
from slam.frontend_manager.handlers.imu_preintegration import ImuPreintegration
from slam.frontend_manager.handlers.pointcloud_matcher import PointcloudMatcher
from slam.frontend_manager.handlers.stereo_odometry import StereoImageOdometry

sensor_handler_table: dict[str, type[ElementHandler]] = {
    "imu1": ImuPreintegration,
    "VLP32_left": PointcloudMatcher,
    "stereo": StereoImageOdometry,
}
