"""Creates a data structure for testing Ros2Reader with S3E-based dataset."""

from dataclasses import dataclass
from pathlib import Path

from rosbags.typesys import Stores, get_typestore

from src.moduslam.data_manager.batch_factory.data_readers.ros2.message_processor import (
    Ros2Humble,
)
from src.moduslam.sensors_factory.configs import (
    ImuConfig,
    Lidar3DConfig,
    MonocularCameraConfig,
    SensorConfig,
    VrsGpsConfig,
)
from src.moduslam.sensors_factory.sensors import (
    Imu,
    Lidar3D,
    MonocularCamera,
    Sensor,
    VrsGps,
)
from src.tests_data_generators.ros2.utils import create_elements, read_messages

imu_name, imu_topic = "Alpha_imu", "/Alpha/imu/data"
lidar_name, lidar_topic = "Alpha_vlp_16", "/Alpha/velodyne_points"
left_camera_name, left_camera_topic = "Alpha_left_camera", "/Alpha/left_camera/compressed"
right_camera_name, right_camera_topic = "Alpha_right_camera", "/Alpha/right_camera/compressed"
rtk_name, rtk_topic = "Alpha_rtk", "/Alpha/fix"

sensors_configs: list[SensorConfig] = [
    ImuConfig(imu_name),
    Lidar3DConfig(lidar_name),
    MonocularCameraConfig(left_camera_name),
    MonocularCameraConfig(right_camera_name),
    VrsGpsConfig(rtk_name),
]


@dataclass
class Sensors:
    """Sensors for S3E-based test dataset."""

    imu = Imu(ImuConfig(imu_name))
    lidar = Lidar3D(Lidar3DConfig(lidar_name))
    left_camera = MonocularCamera(MonocularCameraConfig(left_camera_name))
    right_camera = MonocularCamera(MonocularCameraConfig(right_camera_name))
    rtk = VrsGps(VrsGpsConfig(rtk_name))


class Data:
    """Data structure for S3E-based test dataset."""

    def __init__(self, dataset_path: Path):
        self._topic_sensor_map: dict[str, Sensor] = {
            imu_topic: Sensors.imu,
            lidar_topic: Sensors.lidar,
            left_camera_topic: Sensors.left_camera,
            right_camera_topic: Sensors.right_camera,
            rtk_topic: Sensors.rtk,
        }

        self._type_store = get_typestore(Stores.ROS2_HUMBLE)
        self._msg_processor = Ros2Humble()
        messages = read_messages(dataset_path)
        self.elements = create_elements(
            messages, self._topic_sensor_map, self._msg_processor, self._type_store
        )

        self.sensor_name_topic_map: dict[str, str] = {
            imu_name: imu_topic,
            lidar_name: lidar_topic,
            left_camera_name: left_camera_topic,
            right_camera_name: right_camera_topic,
            rtk_name: rtk_topic,
        }
