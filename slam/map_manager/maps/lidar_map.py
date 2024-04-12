import logging

import numpy as np
import open3d as o3d

logger = logging.getLogger(__name__)


class LidarMap:
    def __init__(self) -> None:
        self._pointcloud = o3d.geometry.PointCloud()

    @property
    def pointcloud(self) -> o3d.geometry.PointCloud:
        return self._pointcloud

    @pointcloud.setter
    def pointcloud(self, pointcloud: o3d.geometry.PointCloud) -> None:
        self._pointcloud = pointcloud

    def set_points(self, points: np.ndarray) -> None:
        """Sets points to the map instance.

        Args:
            points (np.ndarray[Nx3]): points to set.
        """
        self._pointcloud.points = o3d.utility.Vector3dVector(points)
