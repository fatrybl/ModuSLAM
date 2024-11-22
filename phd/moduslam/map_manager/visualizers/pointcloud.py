import open3d as o3d

from moduslam.map_manager.maps.pointcloud import PointcloudMap
from moduslam.map_manager.protocols import MapVisualizer


class PointcloudVisualizer(MapVisualizer):
    """Visualizer for a 3D point cloud."""

    @staticmethod
    def visualize(pointcloud_map: PointcloudMap) -> None:
        """Visualizes the point cloud.

        Args:
            map: point cloud array [N, 3].
        """
        vis = o3d.visualization.Visualizer()
        vis.create_window()
        vis.add_geometry(pointcloud_map.pointcloud)
        vis.run()
