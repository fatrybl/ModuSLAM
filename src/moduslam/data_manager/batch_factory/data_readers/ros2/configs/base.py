from dataclasses import dataclass
from pathlib import Path

from omegaconf import MISSING
from rosbags.typesys import Stores

from src.moduslam.data_manager.batch_factory.configs import DataReaders, DatasetConfig


@dataclass
class Ros2Config(DatasetConfig):
    reader: str = DataReaders.ros2
    name: str = "Any ROS2 Dataset"
    url: str = "Any ROS2 Dataset url"

    directory: Path = MISSING
    ros_distro: Stores = MISSING  # Storage scheme for ROS2 messages
    sensor_topic_mapping: dict[str, str] = MISSING  # unique sensor name -> topic name mapping


@dataclass
class Ros2HumbleConfig(Ros2Config):
    name: str = "S3E: A Multi-Robot Multimodal Dataset for Collaborative SLAM"
    url: str = "https://pengyu-team.github.io/S3E/"

    ros_distro: Stores = Stores.ROS2_HUMBLE  # Storage scheme for ROS2 messages

    directory: Path = MISSING
    sensor_topic_mapping: dict[str, str] = MISSING
