from open3d import geometry, utility

from phd.moduslam.custom_types.numpy import MatrixNx3


class PointCloudMap:
    """A point cloud map."""

    def __init__(self) -> None:
        self._pointcloud = geometry.PointCloud()

    @property
    def pointcloud(self) -> geometry.PointCloud:
        """Point cloud of the map."""
        return self._pointcloud

    @pointcloud.setter
    def pointcloud(self, pointcloud: geometry.PointCloud) -> None:
        """Sets point cloud to the map instance.

        Args:
            pointcloud: point cloud to set.
        """
        self._pointcloud = pointcloud

    def set_points(self, points: MatrixNx3) -> None:
        """Sets points to the map instance.

        Args:
            points:array [N, 3] of points to set.
        """
        self._pointcloud.points = utility.Vector3dVector(points)
