from dataclasses import dataclass, field
from pathlib import Path

from moduslam.system_configs.map_manager.map_factories.lidar_map_factory import (
    LidarMapFactoryConfig,
)


@dataclass
class MapLoaderConfig:
    """Base configuration for map loader."""

    directory: Path = Path("maps")


@dataclass
class LidarMapLoaderConfig(MapLoaderConfig):
    """Configuration for lidar pointcloud map loader."""

    name: str = "lidar_map"
    file_extension: str = "pcd"
    compress: bool = False
    write_ascii: bool = False
    progress_bar: bool = True
    remove_nan: bool = True
    remove_infinity: bool = True


@dataclass
class MapManagerConfig:
    """Base configuration for map manager."""

    map_factory: LidarMapFactoryConfig = field(default_factory=LidarMapFactoryConfig)
    map_loader: LidarMapLoaderConfig = field(default_factory=LidarMapLoaderConfig)
