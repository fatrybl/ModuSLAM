from open3d import geometry, utility

from moduslam.utils.numpy_types import MatrixNx3


class PointcloudMap:
    """Any pointcloud map."""

    def __init__(self) -> None:
        self._pointcloud = geometry.PointCloud()

    @property
    def pointcloud(self) -> geometry.PointCloud:
        """Pointcloud of the map."""
        return self._pointcloud

    @pointcloud.setter
    def pointcloud(self, pointcloud: geometry.PointCloud) -> None:
        """Sets pointcloud to the map instance.

        Args:
            pointcloud: pointcloud to set.
        """
        self._pointcloud = pointcloud

    def set_points(self, points: MatrixNx3) -> None:
        """Sets points to the map instance.

        Args:
            points:array [N, 3] of points to set.
        """
        self._pointcloud.points = utility.Vector3dVector(points)
