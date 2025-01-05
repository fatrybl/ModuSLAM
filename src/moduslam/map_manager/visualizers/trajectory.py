import open3d as o3d

from moduslam.map_manager.maps.trajectory import TrajectoryMap
from moduslam.map_manager.protocols import MapVisualizer


class TrajectoryVisualizer(MapVisualizer):

    @staticmethod
    def visualize(trajectory: TrajectoryMap) -> None:
        """Visualizes the trajectory.

        Args:
            trajectory: trajectory.
        """
        vis = o3d.visualization.Visualizer()
        vis.create_window()

        for pose in trajectory.poses:
            frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.1)
            frame.transform(pose)
            vis.add_geometry(frame)

        # Start the visualization loop
        vis.run()
        vis.destroy_window()
