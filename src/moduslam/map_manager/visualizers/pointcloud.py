import open3d as o3d

from src.moduslam.map_manager.maps.pointcloud import PointCloudMap
from src.moduslam.map_manager.protocols import MapVisualizer


class PointcloudVisualizer(MapVisualizer):
    """Visualizer for a 3D point cloud."""

    @staticmethod
    def visualize(instance: PointCloudMap) -> None:
        """Visualizes the point cloud.

        Args:
            instance: point cloud array [N, 3].
        """
        vis = o3d.visualization.Visualizer()
        vis.create_window()
        vis.add_geometry(instance.pointcloud)
        vis.run()
