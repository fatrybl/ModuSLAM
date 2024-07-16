import open3d as o3d

from moduslam.map_manager.maps.trajectory import TrajectoryMap


class TrajectoryVisualizer:

    @staticmethod
    def visualize(trajectory: TrajectoryMap) -> None:
        """Visualizes the trajectory.

        Args:
            trajectory: trajectory.
        """
        coordinate_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(
            size=0.1, origin=[0, 0, 0]
        )
        vis = o3d.visualization.Visualizer()
        vis.create_window()

        for pose in trajectory.poses:
            coordinate_frame.transform(pose)
            vis.add_geometry(coordinate_frame)

        vis.run()
        vis.destroy_window()
