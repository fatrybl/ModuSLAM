import logging

import numpy as np
import open3d as o3d

logger = logging.getLogger(__name__)


class LidarMap:
    def __init__(self, name: str = "lidar_map"):
        self._name = name
        self._pointcloud = o3d.geometry.PointCloud()

    @property
    def name(self) -> str:
        return self._name

    @property
    def pointcloud(self) -> o3d.geometry.PointCloud:
        return self._pointcloud

    def set_pointcloud(self, points: np.ndarray) -> None:
        """Sets points to the map instance.

        Args:
            points (np.ndarray[Nx3]): points to set.
        """
        self._pointcloud.points = o3d.utility.Vector3dVector(points)

    def save(self) -> None:
        o3d.io.write_point_cloud(
            filename=f"{self._name}.ply",
            pointcloud=self._pointcloud,
            format="ply",
            print_progress=True,
        )
        logger.info(f"Map has been saved to {self._name}.ply")
