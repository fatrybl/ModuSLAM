from collections import defaultdict
from typing import TypeVar

import numpy as np

from phd.moduslam.custom_types.numpy import Matrix4x4, Matrix4xN, MatrixNx3
from phd.moduslam.data_manager.batch_factory.batch import Element
from phd.moduslam.data_manager.batch_factory.factory import BatchFactory
from phd.moduslam.frontend_manager.main_graph.vertices.base import Vertex
from phd.moduslam.utils.auxiliary_methods import check_dimensionality

V = TypeVar("V", bound=Vertex)


def fill_elements(
    vertex_elements_table: dict[V, set[Element]], batch_factory: BatchFactory
) -> dict[V, list[Element]]:
    """Gets elements with raw lidar point cloud measurements and assign to the
    corresponding vertices.

    Args:
        vertex_elements_table: "vertices -> elements" table.
                                Elements do not contain raw lidar point cloud measurements.

        batch_factory: a factory to create the batch.

    Returns:
        "pose -> elements" table.
    """
    table: dict[V, list[Element]] = defaultdict(list)
    for vertex, elements in vertex_elements_table.items():
        elements_list = list(elements)
        batch_factory.fill_batch_with_elements(elements_list)
        table[vertex] = list(batch_factory.batch.data)
        batch_factory.batch.clear()

    return table


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


def convert_pointcloud(pointcloud: MatrixNx3) -> Matrix4xN:
    """Converts a 3D pointcloud to homogeneous coordinates.

    Args:
        pointcloud: pointcloud array [N, 3].

    Returns:
        Homogeneous pointcloud array [4, N].
    """
    pointcloud = pointcloud.T
    ones = np.ones((1, pointcloud.shape[1]))
    pointcloud_homogeneous = np.vstack((pointcloud, ones))
    return pointcloud_homogeneous
