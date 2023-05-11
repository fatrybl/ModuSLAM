from enum import Enum
from pathlib2 import Path

class ConfigFilePaths(Enum):
    left_camera_config = "/configs/.../file_name.yaml"
    right_camera_config = "/configs/.../file_name.yaml"
    imu1_config = "/configs/.../file_name.yaml"