import logging
from collections import defaultdict

import numpy as np

from moduslam.data_manager.batch_factory.batch import Element
from moduslam.frontend_manager.graph.custom_edges import LidarOdometry
from moduslam.frontend_manager.graph.custom_vertices import LidarPose
from moduslam.logger.logging_config import map_manager

logger = logging.getLogger(map_manager)


def map_elements2vertices(
    vertex_edges_table: dict[LidarPose, set[LidarOdometry]]
) -> dict[LidarPose, set[Element]]:
    """Creates "vertex -> elements" table.

    Args:
        vertex_edges_table: "vertex -> edges" table.

    Returns:
        "vertex -> elements" table.
    """
    used_edges: set[LidarOdometry] = set()
    table: dict[LidarPose, set[Element]] = defaultdict(set)

    for vertex, edges in vertex_edges_table.items():
        for edge in edges:
            if edge not in used_edges:
                v1 = edge.vertex1
                v2 = edge.vertex2
                first_element = edge.measurement.elements[0]
                second_element = edge.measurement.elements[1]
                table[v1].add(first_element)
                table[v2].add(second_element)
                used_edges.add(edge)

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
