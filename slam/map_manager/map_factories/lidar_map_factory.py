import logging
from collections import deque

import numpy as np

from slam.data_manager.factory.batch_factory import BatchFactory
from slam.data_manager.factory.element import Element
from slam.frontend_manager.graph.custom_edges import LidarOdometry
from slam.frontend_manager.graph.custom_vertices import LidarPose
from slam.frontend_manager.graph.edge_storage import EdgeStorage
from slam.frontend_manager.graph.vertex_storage import VertexStorage
from slam.logger.logging_config import map_manager
from slam.map_manager.map_factories.utils import (
    create_vertex_elements_table,
    filter_array,
    get_elements,
    transform_pointcloud,
    values_to_array,
)
from slam.map_manager.maps.lidar_map import LidarMap
from slam.setup_manager.sensors_factory.sensors import Lidar3D
from slam.system_configs.map_manager.map_factories.lidar_map_factory import (
    LidarMapFactoryConfig,
)
from slam.utils.numpy_types import Matrix4x4

logger = logging.getLogger(map_manager)


class LidarMapFactory:
    """Factory for a lidar map."""

    def __init__(self, config: LidarMapFactoryConfig) -> None:
        """
        Args:
            config: configuration of the factory.
        """
        self._map = LidarMap()
        self._required_vertex_type = LidarPose
        self._num_channels: int = config.num_channels
        self._min_range: float = config.min_range
        self._max_range: float = config.max_range

    @property
    def map(self) -> LidarMap:
        """Lidar pointcloud map instance."""
        return self._map

    def create(
        self, vertex_storage: VertexStorage, edge_storage: EdgeStorage, batch_factory: BatchFactory
    ) -> None:
        """Creates a lidar pointcloud map.

        Args:
            vertex_storage: storage of graph vertices.

            edge_storage: storage of graph edges.

            batch_factory: factory to create a data batch.
        """
        vertices = vertex_storage.get_vertices(self._required_vertex_type)
        edges = {edge for edge in edge_storage.edges if isinstance(edge, LidarOdometry)}
        table = create_vertex_elements_table(vertices, edges)
        table_with_data = get_elements(table, batch_factory)
        pointcloud = self._build_pointcloud_map(table_with_data)
        self._map.set_points(pointcloud)

    def _build_pointcloud(
        self, pose: Matrix4x4, tf: Matrix4x4, values: tuple[float, ...]
    ) -> np.ndarray:
        """Builds a pointcloud from the given values and transforms it according to the
        vertex pose and base -> lidar transformation. Ignores intensity values.

        Args:
            pose: pose SE(3).

            tf: base -> lidar transformation SE(3).

            values: raw lidar pointcloud data.

        Returns:
            Pointcloud array [4, N].
        """
        pointcloud = values_to_array(values, self._num_channels)
        pointcloud = filter_array(pointcloud, self._min_range, self._max_range)
        pointcloud[3, :] = 1  # ignore intensity values
        pointcloud = transform_pointcloud(pose, tf, pointcloud)
        return pointcloud

    def _build_pointcloud_map(
        self, vertex_elements_table: dict[LidarPose, deque[Element]]
    ) -> np.ndarray:
        """Builds a pointcloud map from the given "vertex -> elements" table.

        Args:
            vertex_elements_table: "vertex -> elements" table.

        Returns:
            Pointcloud map array [N,3].

        Raises:
            TypeError: if the sensor is not of type Lidar3D.
        """
        pointcloud_map = np.empty((4, 0))

        for vertex, elements in vertex_elements_table.items():
            for element in elements:
                sensor = element.measurement.sensor

                if isinstance(sensor, Lidar3D):

                    pointcloud = self._build_pointcloud(
                        pose=vertex.value,
                        tf=sensor.tf_base_sensor,
                        values=element.measurement.values,
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
