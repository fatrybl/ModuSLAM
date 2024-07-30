from dataclasses import dataclass

from moduslam.system_configs.map_manager.map_manager import MapFactoryConfig
from moduslam.system_configs.map_manager.map_types import MapType


@dataclass
class LidarMapFactoryConfig(MapFactoryConfig):
    """Lidar pointcloud map factory configuration."""

    map_type: str = MapType.lidar_pointcloud
    num_channels: int = 4
    min_range: float = 5
    max_range: float = 100
