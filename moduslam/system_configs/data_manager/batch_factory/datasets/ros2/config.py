# TODO: Create configuration file for ros2

from dataclasses import dataclass, field
from pathlib import Path

from moduslam.system_configs.data_manager.batch_factory.data_readers import DataReaders
from moduslam.system_configs.data_manager.batch_factory.datasets.base_dataset import (
    DatasetConfig,
)

@dataclass
class Ros2Config(DatasetConfig):
    """Ros2 Rosbag Dataset parameters."""

    directory: Path = Path()

    sensors_table: dict[str, str] = field(default_factory=lambda: {})

    topics_table: dict[str, str]= field(default_factory=lambda: {})
    # data_types: list[str] = field(default_factory=lambda: [])

    reader: str = DataReaders.ros2_reader

    name: str = "Ros2 Reader for Ros2bags"

    url: str = "example.com"


