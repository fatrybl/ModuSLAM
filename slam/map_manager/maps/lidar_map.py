import logging

import numpy as np
import open3d as o3d

logger = logging.getLogger(__name__)


class LidarMap:
    """Lidar pointcloud map."""

    def __init__(self) -> None:
        self._pointcloud = o3d.geometry.PointCloud()

    @property
    def pointcloud(self) -> o3d.geometry.PointCloud:
        """Pointcloud of the map."""
        return self._pointcloud

    @pointcloud.setter
    def pointcloud(self, pointcloud: o3d.geometry.PointCloud) -> None:
        """Sets pointcloud to the map instance.

        Args:
            pointcloud: pointcloud to set.
        """
        self._pointcloud = pointcloud

    def set_points(self, points: np.ndarray) -> None:
        """Sets points to the map instance.

        Args:
            points:array [N, 3] of points to set.
        """
        self._pointcloud.points = o3d.utility.Vector3dVector(points)
