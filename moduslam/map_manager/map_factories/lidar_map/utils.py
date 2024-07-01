import logging
from collections import defaultdict

import numpy as np
import open3d as o3d

from moduslam.data_manager.batch_factory.batch import Element
from moduslam.frontend_manager.graph.custom_edges import LidarOdometry
from moduslam.frontend_manager.graph.custom_vertices import LidarPose
from moduslam.logger.logging_config import map_manager
from moduslam.utils.deque_set import DequeSet

logger = logging.getLogger(map_manager)


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


def create_vertex_elements_table(
    vertices: DequeSet[LidarPose], edges: set[LidarOdometry]
) -> dict[LidarPose, set[Element]]:
    """Creates "vertex -> elements" table.

    Args:
        vertices: vertices to get elements for.

        edges: edges to check.

    Returns:
        "vertex -> elements" table.
    """

    table: dict[LidarPose, set[Element]] = defaultdict(set)

    num_poses = len(vertices)

    for i, vertex in enumerate(vertices):
        if i == num_poses - 1:
            for e in vertex.edges:
                if isinstance(e, LidarOdometry):
                    m = e.measurements[0]
                    element = m.elements[1]
                    table[vertex].add(element)
        else:
            for e in vertex.edges:
                if e in edges and isinstance(e, LidarOdometry):
                    m = e.measurements[0]
                    element = m.elements[0]
                    table[vertex].add(element)
                    edges.remove(e)
    return table


def values_to_array(values: tuple[float, ...], num_channels: int) -> np.ndarray:
    """Converts values to pointcloud np.ndarray [num_channels, N].

    Args:
        values: values to convert.

        num_channels: number of channels in pointcloud.

    Returns:
        Values as array [num_channels, N].
    """
    array = np.array(values).reshape((-1, num_channels)).T
    return array
