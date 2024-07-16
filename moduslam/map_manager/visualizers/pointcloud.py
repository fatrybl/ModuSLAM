import open3d as o3d


class PointcloudVisualizer:
    """Visualizer for the lidar pointcloud."""

    @staticmethod
    def visualize(pointcloud: o3d.geometry.PointCloud) -> None:
        """Visualizes the pointcloud.

        Args:
            pointcloud: pointcloud array [N, 3].
        """
        vis = o3d.visualization.Visualizer()
        vis.create_window()
        vis.add_geometry(pointcloud)
        vis.run()
