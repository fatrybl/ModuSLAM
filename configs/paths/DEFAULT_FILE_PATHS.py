from enum import Enum


class ConfigFilePaths(Enum):
    cfg_directory_path = "/configs"
    left_camera_config = "/configs/sensors/left_rgb_camera.yaml"
    right_camera_config = "/configs/sensors/right_rgb_camera.yaml"
    imu1_config = "/configs/sensors/imu.yaml"
    data_manager_config = "/configs/system/data_manager.yaml"
