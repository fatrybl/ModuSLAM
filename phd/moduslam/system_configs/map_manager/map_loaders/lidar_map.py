from dataclasses import dataclass

from moduslam.system_configs.map_manager.map_manager import MapLoaderConfig


@dataclass
class LidarMapLoaderConfig(MapLoaderConfig):
    """Configuration for lidar pointcloud map loader."""

    map_type: str = "lidar_pointcloud"
    name: str = "lidar_map"
    file_extension: str = "pcd"
    compress: bool = False
    write_ascii: bool = False
    progress_bar: bool = True
    remove_nan: bool = True
    remove_infinity: bool = True
