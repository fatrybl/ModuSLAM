import logging
from collections import defaultdict

import numpy as np
from open3d import geometry, utility

from src.custom_types.aliases import Matrix4x4
from src.custom_types.numpy import MatrixMxN
from src.logger.logging_config import map_manager
from src.measurement_storage.measurements.pose_odometry import OdometryWithElements
from src.moduslam.data_manager.batch_factory.batch import Element
from src.moduslam.frontend_manager.main_graph.edges.base import Edge
from src.moduslam.frontend_manager.main_graph.edges.pose_odometry import PoseOdometry
from src.moduslam.frontend_manager.main_graph.vertices.custom import Pose
from src.moduslam.map_manager.map_factories.lidar_map.config import (
    LidarPointCloudConfig,
)
from src.moduslam.map_manager.map_factories.utils import filter_array
from src.moduslam.sensors_factory.sensors import Lidar3D

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


def create_3d_point_cloud(
    tf: Matrix4x4, values: tuple[float, ...], config: LidarPointCloudConfig
) -> geometry.PointCloud:
    """Creates a 3D point cloud from raw measurement.

    Args:
        tf: base->sensor SE(3) transformation.

        values: raw lidar point cloud data.

        config: a configuration for lidar point cloud.

    Returns:
        a 3D point cloud.
    """
    tf_array = np.array(tf)
    points = values_to_array(values, config.num_channels)
    points = filter_array(points, config.min_range, config.max_range)
    points = points[:, :-1]  # remove unnecessary 4-th channel.

    cloud = geometry.PointCloud()
    cloud.points = utility.Vector3dVector(points)
    cloud.transform(tf_array)

    return cloud


def create_point_cloud_from_element(
    element: Element, config: LidarPointCloudConfig
) -> geometry.PointCloud:
    """Creates a 3D point cloud array from the element with Lidar measurement.

    Args:
        element: an element with lidar measurement.

        config: a configuration for point cloud creation.

    Returns:
        a 3D point cloud.

    Raises:
        ValueError: if the element does not contain a valid lidar measurement.
    """
    sensor = element.measurement.sensor
    values = element.measurement.values

    if isinstance(sensor, Lidar3D) and values is not None:
        cloud = create_3d_point_cloud(sensor.tf_base_sensor, values, config)
        return cloud

    else:
        raise TypeError("The element does not contain a valid lidar measurement.")
