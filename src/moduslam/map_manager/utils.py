from pathlib import Path

import open3d as o3d

from src.moduslam.data_manager.batch_factory.readers.kaist.utils import read_binary
from src.moduslam.map_manager.map_factories.lidar_map.utils import values_to_array


def read_4_channel_bin_pcd(file_path: Path) -> o3d.geometry.PointCloud:
    """Load a binary file with points data and creates a point cloud.

    Args:
        file_path: path to the binary file.

    Returns:
        a point cloud.
    """
    data = read_binary(file_path)
    points = values_to_array(data, 4)
    points = points[:, :3]
    cloud = o3d.geometry.PointCloud()
    cloud.points = o3d.utility.Vector3dVector(points)
    return cloud
