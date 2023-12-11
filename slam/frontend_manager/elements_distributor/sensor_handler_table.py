from typing import Type

from slam.frontend_manager.handlers.ABC_module import ElementHandler
from slam.frontend_manager.handlers.imu_preintegration.imu_preintegration import ImuPreintegration
from slam.frontend_manager.handlers.pointcloid_registration.pointcloud_matcher import KissICP
from slam.frontend_manager.handlers.stereo_camera_feature_tracking.feature_tracking import FeatureTracker
from slam.setup_manager.sensor_factory.sensors import Sensor, Imu, StereoCamera, Lidar3D

sensor_handler_table: dict[Type[Sensor], tuple[Type[ElementHandler]]] = {
    Imu: ImuPreintegration,
    StereoCamera: FeatureTracker,
    Lidar3D: KissICP
}
