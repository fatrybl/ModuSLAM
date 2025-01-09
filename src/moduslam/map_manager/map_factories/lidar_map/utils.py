import logging
from collections import defaultdict

import numpy as np

from src.custom_types.numpy import MatrixMxN
from src.logger.logging_config import map_manager
from src.measurement_storage.measurements.pose_odometry import OdometryWithElements
from src.moduslam.data_manager.batch_factory.batch import Element
from src.moduslam.frontend_manager.main_graph.edges.base import Edge
from src.moduslam.frontend_manager.main_graph.edges.pose_odometry import PoseOdometry
from src.moduslam.frontend_manager.main_graph.vertices.custom import Pose

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
        LookupError: none of edge`s vertices is a key in the input table.
    """
    table: dict[Pose, set[Element]] = defaultdict(set)

    for current_pose, edges in vertex_edges_table.items():
        for edge in edges:
            measurement = edge.measurement
            pose1, pose2 = edge.vertex1, edge.vertex2

            if isinstance(measurement, OdometryWithElements):
                el1 = measurement.elements[0]
                el2 = measurement.elements[1]

                if current_pose is pose1:
                    table[current_pose].add(el1)
                elif current_pose is pose2:
                    table[current_pose].add(el2)
                else:
                    raise LookupError(f"Current pose {current_pose} is not in the edge {edge}")
    return table


def values_to_array(values: tuple[float, ...], num_channels: int) -> MatrixMxN:
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
    table: defaultdict[Pose, set[PoseOdometry]] = defaultdict(set)

    for vertex, edges in pose_edges_table.items():
        for edge in edges:
            m = edge.measurement
            if isinstance(edge, PoseOdometry) and isinstance(m, OdometryWithElements):
                table[vertex].add(edge)

    return table
