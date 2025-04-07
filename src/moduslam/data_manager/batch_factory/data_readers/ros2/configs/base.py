from dataclasses import dataclass
from pathlib import Path

from omegaconf import MISSING
from rosbags.typesys import Stores

from src.moduslam.data_manager.batch_factory.configs import DataReaders, DatasetConfig


@dataclass
class Ros2Config(DatasetConfig):
    reader: str = DataReaders.ros2_reader
    name: str = "Any ROS2 Dataset"
    url: str = "Any ROS2 Dataset url"

    ros_distro: Stores = Stores.LATEST  # Storage scheme for ROS2 messages

    directory: Path = MISSING
    sensor_topic_mapping: dict[str, str] = MISSING  # unique sensor name -> topic name mapping


@dataclass
class Ros2Humble(Ros2Config):
    name: str = "S3E: A Multi-Robot Multimodal Dataset for Collaborative SLAM"
    url: str = "https://pengyu-team.github.io/S3E/"

    ros_distro: Stores = Stores.ROS2_HUMBLE  # Storage scheme for ROS2 messages

    directory: Path = MISSING
    sensor_topic_mapping: dict[str, str] = MISSING
