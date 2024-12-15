import logging
from collections import defaultdict
from collections.abc import Iterable

import numpy as np

from phd.logger.logging_config import map_manager
from phd.measurement_storage.measurements.pose_odometry import OdometryWithElements
from phd.moduslam.data_manager.batch_factory.batch import Element
from phd.moduslam.frontend_manager.main_graph.edges.pose_odometry import PoseOdometry
from phd.moduslam.frontend_manager.main_graph.graph import Graph
from phd.moduslam.frontend_manager.main_graph.vertices.custom import Pose

logger = logging.getLogger(map_manager)


def map_elements2vertices(
    vertex_edges_table: dict[Pose, set[PoseOdometry]]
) -> dict[Pose, set[Element]]:
    """Creates "vertex -> elements" table.

    Args:
        vertex_edges_table: "vertex -> edges" table.

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
    """Converts values to pointcloud np.ndarray [num_channels, N].

    Args:
        values: values to convert.

        num_channels: number of channels in pointcloud.

    Returns:
        Values as array [num_channels, N].
    """
    array = np.array(values).reshape((-1, num_channels)).T
    return array


def create_vertex_edges_table(
    graph: Graph, vertices: Iterable[Pose]
) -> dict[Pose, set[PoseOdometry]]:
    """Creates a table with vertices and corresponding edges.

    Args:
        graph: graph to create a table from.

        vertices: vertices to create a table for.
    Returns:
        "pose -> pose odometries" table.
    """
    table: dict[Pose, set[PoseOdometry]] = {}

    for vertex in vertices:
        edges = graph.get_connected_edges(vertex)
        for edge in edges:
            if isinstance(edge, PoseOdometry) and isinstance(
                edge.measurement, OdometryWithElements
            ):
                if vertex not in table:
                    table[vertex] = {edge}
                else:
                    table[vertex].add(edge)

    return table
