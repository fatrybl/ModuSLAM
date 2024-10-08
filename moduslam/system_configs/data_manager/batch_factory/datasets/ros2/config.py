# TODO: Create configuration file for ros2

from dataclasses import dataclass, field
from pathlib import Path

from moduslam.system_configs.data_manager.batch_factory.data_readers import DataReaders
from moduslam.system_configs.data_manager.batch_factory.datasets.base_dataset import (
    DatasetConfig,
)
from moduslam.system_configs.data_manager.batch_factory.datasets.ros2.paths import (
    Ros2DatasetPathConfig as Ros2Paths,
)


@dataclass
class Ros2Config(DatasetConfig):
    """Ros2 Rosbag Dataset parameters."""

    directory: Path = field(kw_only=True)

    sensors_table: dict[str, str] = field(default_factory=lambda: {})

    data_stamp_file: Path = Ros2Paths.data_stamp

    reader: str = DataReaders.ros2_reader

    name: str = "Ros2 Reader for Ros2bags"

    url: str = "example.com"
