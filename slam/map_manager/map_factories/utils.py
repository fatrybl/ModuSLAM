from collections import defaultdict, deque

import numpy as np

from slam.data_manager.factory.batch_factory import BatchFactory
from slam.data_manager.factory.element import Element
from slam.frontend_manager.graph.custom_edges import LidarOdometry
from slam.frontend_manager.graph.custom_vertices import LidarPose
from slam.utils.auxiliary_methods import check_dimensionality
from slam.utils.deque_set import DequeSet
from slam.utils.numpy_types import Matrix4x4


def get_elements(
    vertex_elements_table: dict[LidarPose, set[Element]], batch_factory: BatchFactory
) -> dict[LidarPose, deque[Element]]:
    """Gets elements with raw lidar pointcloud measurements and assign to the
    corresponding vertices.

    Args:
        vertex_elements_table: "vertices -> elements" table.
                                Elements do not contain raw lidar pointcloud measurements.

        batch_factory (BatchFactory): factory to create a batch.

    Returns:
        "vertices -> elements" table. Each element contains raw lidar pointcloud measurement.
    """
    table: dict[LidarPose, deque[Element]] = defaultdict(deque)
    for vertex, elements in vertex_elements_table.items():
        batch_factory.create_batch(elements)  # type: ignore
        table[vertex] = batch_factory.batch.data

    return table


def create_vertex_elements_table(
    vertices: DequeSet[LidarPose], edges: set[LidarOdometry]
) -> dict[LidarPose, set[Element]]:
    """Creates "vertex -> elements" table.

    Args:
        vertices: vertices to get elements for.

        edges: LidarOdometry edges to check.

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


def transform_pointcloud(tf1: Matrix4x4, tf2: Matrix4x4, pointcloud: np.ndarray) -> np.ndarray:
    """Transforms points` coordinates to the global coordinate frame based
        on the given vertex pose and transformation: base -> sensor.

    Args:
        tf1: transformation matrix SE(3).

        tf2: transformation matrix SE(3).

        pointcloud: pointcloud array [4, N] to transform.

    Returns:
        Transformed pointcloud array [4, N].
    """
    result = tf1 @ tf2 @ pointcloud
    return result


def filter_array(array: np.ndarray, lower_bound: float, upper_bound: float) -> np.ndarray:
    """Filters 2D array [4, N] with lower/upper bounds. If a column has at least one
    value outside the bounds, the whole column is removed.

    Args:
        array: array [4, N] of points to filter.

        lower_bound: lower bound value.

        upper_bound: upper bound value.

    Returns:
        filtered array [4, K].
    """
    check_dimensionality(array, shape=(4, array.shape[1]))

    mask = np.any((array[:3, :] >= lower_bound) & (array[:3, :] <= upper_bound), axis=0)
    filtered_arr = array[:, mask]
    return filtered_arr
