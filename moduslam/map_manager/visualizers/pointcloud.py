import open3d as o3d

from moduslam.map_manager.protocols import MapVisualizer


class PointcloudVisualizer(MapVisualizer):
    """Visualizer for a 3D pointcloud."""

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
