import logging
from collections import deque

import numpy as np

from moduslam.data_manager.batch_factory.batch import Element
from moduslam.data_manager.batch_factory.factory import BatchFactory
from moduslam.frontend_manager.graph.custom_edges import LidarOdometry
from moduslam.frontend_manager.graph.custom_vertices import LidarPose
from moduslam.frontend_manager.graph.graph import Graph
from moduslam.logger.logging_config import map_manager
from moduslam.map_manager.map_factories.lidar_map.utils import (
    map_elements2vertices,
    values_to_array,
)
from moduslam.map_manager.map_factories.utils import (
    create_vertex_edges_table,
    fill_elements,
    filter_array,
    transform_pointcloud,
)
from moduslam.map_manager.maps.pointcloud import PointcloudMap
from moduslam.map_manager.protocols import MapFactory
from moduslam.setup_manager.sensors_factory.sensors import Lidar3D
from moduslam.system_configs.map_manager.map_factories.lidar_map import (
    LidarMapFactoryConfig,
)
from moduslam.types.aliases import Matrix4x4

logger = logging.getLogger(map_manager)


class LidarMapFactory(MapFactory):
    """Factory for a lidar map."""

    def __init__(self, config: LidarMapFactoryConfig) -> None:
        """
        Args:
            config: configuration of the factory.
        """
        self._map = PointcloudMap()
        self._num_channels: int = config.num_channels
        self._min_range: float = config.min_range
        self._max_range: float = config.max_range

    @property
    def map(self) -> PointcloudMap:
        """Lidar point cloud map instance."""
        return self._map

    def create_map(
        self, graph: Graph[LidarPose, LidarOdometry], batch_factory: BatchFactory
    ) -> None:
        """Creates a lidar point cloud map.

        Args:
            graph: graph to create a map from.

            batch_factory: factory to create a data batch.
        """
        vertices = graph.vertex_storage.get_vertices(LidarPose)
        vertex_edges_table = create_vertex_edges_table(graph, vertices, LidarOdometry)
        table1 = map_elements2vertices(vertex_edges_table)
        table2 = fill_elements(table1, batch_factory)
        points_map = self._create_points_map(table2)
        self._map.set_points(points_map)

    def _create_points_map(
        self, vertex_elements_table: dict[LidarPose, deque[Element]]
    ) -> np.ndarray:
        """Creates a points map from the given "vertex -> elements" table.

        Args:
            vertex_elements_table: "vertex -> elements" table.

        Returns:
            Points map array [N,3].

        Raises:
            TypeError: if the sensor is not of type Lidar3D.
        """
        pointcloud_map = np.empty(shape=(4, 0))

        for vertex, elements in vertex_elements_table.items():
            for element in elements:
                sensor = element.measurement.sensor

                if isinstance(sensor, Lidar3D):
                    pointcloud = self._create_pointcloud(
                        vertex.value, sensor.tf_base_sensor, element.measurement.values
                    )
                    pointcloud_map = np.concatenate((pointcloud_map, pointcloud), axis=1)

                else:
                    msg = (
                        f"Sensor is of type {type(sensor).__name__!r} but not {Lidar3D.__name__!r}"
                    )
                    logger.error(msg)
                    raise TypeError(msg)

        pointcloud_map = pointcloud_map[:3, :].T  # ignore intensity values.
        return pointcloud_map

    def _create_pointcloud(
        self, pose: Matrix4x4, tf: list[list[float]], values: tuple[float, ...]
    ) -> np.ndarray:
        """Creates a pointcloud from the given values and transforms it according to the
        vertex pose and base -> lidar transformation. Ignores intensity values.

        Args:
            pose: pose SE(3).

            tf: base -> lidar transformation SE(3).

            values: raw lidar point cloud data.

        Returns:
            Point cloud array [4, N].
        """
        tf_array = np.array(tf)
        pose_array = np.array(pose)
        pointcloud = values_to_array(values, self._num_channels)
        pointcloud = filter_array(pointcloud, self._min_range, self._max_range)
        pointcloud[3, :] = 1  # ignore intensity values
        pointcloud = transform_pointcloud(pose_array, tf_array, pointcloud)
        return pointcloud
