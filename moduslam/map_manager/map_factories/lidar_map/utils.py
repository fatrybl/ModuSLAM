import logging
from collections import defaultdict
from collections.abc import Sequence

import numpy as np

from moduslam.data_manager.batch_factory.batch import Element
from moduslam.frontend_manager.graph.custom_edges import LidarOdometry
from moduslam.frontend_manager.graph.custom_vertices import LidarPose
from moduslam.logger.logging_config import map_manager

logger = logging.getLogger(map_manager)


def create_vertex_elements_table(
    vertices: Sequence[LidarPose],
    vertex_edges_table: dict[LidarPose, set[LidarOdometry]],
) -> dict[LidarPose, set[Element]]:
    """Creates "vertex -> elements" table.

    Args:
        vertices: vertices to get elements for.

        vertex_edges_table: "vertex -> edges" table.

    Returns:
        "vertex -> elements" table.
    """

    table: dict[LidarPose, set[Element]] = defaultdict(set)
    num_poses = len(vertices)

    for i, vertex in enumerate(vertices):
        vertex_edges = vertex_edges_table[vertex]
        if i == num_poses - 1:
            for edge in vertex_edges:
                element = edge.measurement.elements[1]
                table[vertex].add(element)
        else:
            for edge in vertex_edges:
                element = edge.measurement.elements[0]
                table[vertex].add(element)
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
