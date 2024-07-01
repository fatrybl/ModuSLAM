import logging
from collections import deque

import numpy as np

from moduslam.data_manager.batch_factory.batch import Element
from moduslam.data_manager.batch_factory.factory import BatchFactory
from moduslam.frontend_manager.graph.custom_edges import LidarOdometry
from moduslam.frontend_manager.graph.custom_vertices import LidarPose
from moduslam.frontend_manager.graph.edge_storage import EdgeStorage
from moduslam.frontend_manager.graph.vertex_storage import VertexStorage
from moduslam.logger.logging_config import map_manager
from moduslam.map_manager.map_factories.lidar_map.utils import (
    create_vertex_elements_table,
    values_to_array,
)
from moduslam.map_manager.map_factories.utils import (
    filter_array,
    get_elements,
    transform_pointcloud,
)
from moduslam.map_manager.maps.pointcloud_map import PointcloudMap
from moduslam.setup_manager.sensors_factory.sensors import Lidar3D
from moduslam.system_configs.map_manager.map_factories.lidar_map_factory import (
    LidarMapFactoryConfig,
)
from moduslam.utils.numpy_types import Matrix4x4

logger = logging.getLogger(map_manager)


class LidarMapFactory:
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
        vertices = vertex_storage.get_vertices(LidarPose)
        edges = {edge for edge in edge_storage.edges if isinstance(edge, LidarOdometry)}
        table1 = create_vertex_elements_table(vertices, edges)
        table2 = get_elements(table1, batch_factory)
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

    def _create_pointcloud(
        self, pose: Matrix4x4, tf: Matrix4x4, values: tuple[float, ...]
    ) -> np.ndarray:
        """Creates a pointcloud from the given values and transforms it according to the
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
