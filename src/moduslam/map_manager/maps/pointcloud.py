from open3d import geometry


class PointCloudMap:
    """A point cloud map."""

    def __init__(self) -> None:
        self._pointcloud = geometry.PointCloud()

    @property
    def pointcloud(self) -> geometry.PointCloud:
        """3D point cloud."""
        return self._pointcloud

    @pointcloud.setter
    def pointcloud(self, pointcloud: geometry.PointCloud) -> None:
        """Sets point cloud to the map instance.

        Args:
            pointcloud: a 3D point cloud to set.
        """
        self._pointcloud = pointcloud
