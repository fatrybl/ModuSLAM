from collections import defaultdict
from typing import TypeVar

import numpy as np

from phd.moduslam.custom_types.numpy import Matrix4x4, Matrix4xN, MatrixNx3, MatrixNx4
from phd.moduslam.data_manager.batch_factory.batch import Element
from phd.moduslam.data_manager.batch_factory.factory import BatchFactory
from phd.moduslam.frontend_manager.main_graph.vertices.base import Vertex
from phd.utils.auxiliary_methods import check_dimensionality

V = TypeVar("V", bound=Vertex)


def fill_elements(
    vertex_elements_table: dict[V, set[Element]], batch_factory: BatchFactory
) -> dict[V, list[Element]]:
    """Creates a table with vertices and elements with raw measurements.

    Args:
        vertex_elements_table: a table of vertices and elements w/o raw measurements.

        batch_factory: a factory to create get raw measurements for elements.

    Returns:
        "vertex -> elements" table.
    """
    table: dict[V, list[Element]] = defaultdict(list)
    for vertex, elements in vertex_elements_table.items():
        elements_list = list(elements)
        batch_factory.fill_batch_with_elements(elements_list)
        table[vertex] = list(batch_factory.batch.data)
        batch_factory.batch.clear()

    return table


def transform_pointcloud(tf1: Matrix4x4, tf2: Matrix4x4, point_cloud: MatrixNx4) -> MatrixNx4:
    """Applies transformations to the point cloud.

    Args:
        tf1: transformation matrix SE(3).

        tf2: transformation matrix SE(3).

        point_cloud: point cloud array [N, 4] to transform.

    Returns:
        transformed point_cloud array [N, 4].
    """
    result = tf1 @ tf2 @ point_cloud.T
    return result.T


def filter_array(array: MatrixNx4, lower_bound: float, upper_bound: float) -> MatrixNx4:
    """Filters 2D array [N, 4] with lower/upper bounds. If a column has at least one
    value outside the bounds, the whole column is removed.

    Args:
        array: array [N, 4] of points to filter.

        lower_bound: lower bound value.

        upper_bound: upper bound value.

    Returns:
        filtered array [K, 4].
    """
    n, m = array.shape[0], 4
    check_dimensionality(array, shape=(n, m))

    mask = np.any((array[:, :-1] >= lower_bound) & (array[:, :-1] <= upper_bound), axis=1)
    filtered_arr = array[mask, :]
    return filtered_arr


def convert_pointcloud(point_cloud: MatrixNx3) -> Matrix4xN:
    """Converts a 3D point cloud to homogeneous coordinates.

    Args:
        point_cloud: point cloud array [N, 3].

    Returns:
        homogeneous point cloud array [4, N].
    """
    point_cloud = point_cloud.T
    ones = np.ones((1, point_cloud.shape[1]))
    pointcloud_homogeneous = np.vstack((point_cloud, ones))
    return pointcloud_homogeneous
