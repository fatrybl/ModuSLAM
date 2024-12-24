import logging
from collections import defaultdict

import numpy as np

from phd.logger.logging_config import map_manager
from phd.measurement_storage.measurements.pose_odometry import OdometryWithElements
from phd.moduslam.data_manager.batch_factory.batch import Element
from phd.moduslam.frontend_manager.main_graph.edges.base import Edge
from phd.moduslam.frontend_manager.main_graph.edges.pose_odometry import PoseOdometry
from phd.moduslam.frontend_manager.main_graph.vertices.custom import Pose

logger = logging.getLogger(map_manager)


def map_elements2vertices(
    vertex_edges_table: dict[Pose, set[PoseOdometry]]
) -> dict[Pose, set[Element]]:
    """Creates "pose -> elements" table.

    Args:
        vertex_edges_table: poses with PoseOdometry edges.

    Returns:
        "pose -> elements" table.

    Raises:
        TypeError: if odometry measurement is not of type OdometryWithElements".
    """
    used_edges: set[PoseOdometry] = set()
    table: dict[Pose, set[Element]] = defaultdict(set)

    for vertex, edges in vertex_edges_table.items():
        for edge in edges:
            if edge not in used_edges:
                v1 = edge.vertex1
                v2 = edge.vertex2

                measurement = edge.measurement
                if isinstance(measurement, OdometryWithElements):
                    first_element = measurement.elements[0]
                    second_element = measurement.elements[1]
                    table[v1].add(first_element)
                    table[v2].add(second_element)
                    used_edges.add(edge)
                else:
                    raise TypeError(f"Measurement{measurement} is not of type OdometryWithElements")

    return table


def values_to_array(values: tuple[float, ...], num_channels: int) -> np.ndarray:
    """Converts raw values to point cloud arrays [N, num_channels].

    Args:
        values: values to convert.

        num_channels: a number of channels in point cloud.

    Returns:
        array [N, num_channels].
    """
    array = np.array(values).reshape((-1, num_channels))
    return array


def create_pose_edges_table(
    pose_edges_table: dict[Pose, set[Edge]]
) -> dict[Pose, set[PoseOdometry]]:
    """Creates a table with poses and edges containing data elements.

    Args:
        pose_edges_table: "pose -> edges" table.

    Returns:
        "pose -> pose odometries" table.
    """
    table: dict[Pose, set[PoseOdometry]] = {}

    for vertex, edges in pose_edges_table.items():
        for edge in edges:
            if isinstance(edge, PoseOdometry) and isinstance(
                edge.measurement, OdometryWithElements
            ):
                if vertex not in table:
                    table[vertex] = {edge}
                else:
                    table[vertex].add(edge)

    return table
