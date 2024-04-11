import open3d as o3d


class PointcloudVisualizer:

    @staticmethod
    def visualize(pointcloud: o3d.geometry.PointCloud) -> None:
        """Visualizes the pointcloud.

        Args:
            pointcloud (np.ndarray[N,3]): pointcloud to visualize.
        """
        vis = o3d.visualization.Visualizer()
        vis.create_window()
        vis.add_geometry(pointcloud)
        vis.run()
