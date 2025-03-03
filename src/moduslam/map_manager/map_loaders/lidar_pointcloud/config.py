from dataclasses import dataclass


@dataclass
class LidarMapLoaderConfig:
    """Configuration for lidar pointcloud map loader."""

    directory: str = "/home/mark/Desktop/PhD/ModuSLAM/final_experiments/"
    name: str = "lidar_map"
    file_extension: str = "ply"
    compress: bool = False
    write_ascii: bool = False
    progress_bar: bool = True
    remove_nan: bool = True
    remove_infinity: bool = True
