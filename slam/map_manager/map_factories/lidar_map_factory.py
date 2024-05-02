import logging
from collections import defaultdict, deque
from collections.abc import Iterable

import numpy as np

from slam.data_manager.factory.batch_factory import BatchFactory
from slam.data_manager.factory.element import Element
from slam.frontend_manager.graph.base_edges import Edge
from slam.frontend_manager.graph.base_vertices import Vertex
from slam.frontend_manager.graph.custom_edges import LidarOdometry
from slam.frontend_manager.graph.custom_vertices import LidarPose
from slam.frontend_manager.graph.vertex_storage import VertexStorage
from slam.frontend_manager.measurement_storage import Measurement
from slam.logger.logging_config import map_manager_logger
from slam.map_manager.maps.lidar_map import LidarMap
from slam.setup_manager.sensors_factory.sensors import Lidar3D
from slam.system_configs.map_manager.map_factories.lidar_map_factory import (
    LidarMapFactoryConfig,
)
from slam.utils.auxiliary_methods import check_dimensionality
from slam.utils.deque_set import DequeSet
from slam.utils.numpy_types import Matrix4x4

logger = logging.getLogger(map_manager_logger)


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

    @property
    def vertices_types(self) -> tuple[type[Vertex], ...]:
        """Required vertices types to create a lidar pointcloud map."""
        return (self._required_vertex_type,)

    def create(self, vertex_storage: VertexStorage, batch_factory: BatchFactory) -> None:
        """Creates a lidar pointcloud map.

        Args:
            vertex_storage: storage of graph vertices.

            batch_factory: factory to create a data batch.
        """
        table = self._create_requests_table(vertex_storage)
        table_with_data = self._get_elements(table, batch_factory)
        pointcloud = self._build_pointcloud_map(table_with_data)
        self._map.set_points(pointcloud)

    def _create_requests_table(
        self, vertex_storage: VertexStorage
    ) -> dict[LidarPose, set[Element]]:
        """Creates "vertices -> elements" table.

        Args:
            vertex_storage: storage of graph vertices.

        Returns:
            "vertices -> elements" table.
        """
        vertices: DequeSet[LidarPose] = vertex_storage.get_vertices(self._required_vertex_type)
        vertex_edges_table: dict[LidarPose, set[Edge]] = {v: v.edges for v in vertices}
        vertex_measurements_table = self._create_vertex_measurements_table(vertex_edges_table)
        vertex_elements_table = self._create_vertex_elements_table(vertex_measurements_table)
        return vertex_elements_table

    @staticmethod
    def _get_elements(
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

    @staticmethod
    def _create_vertex_measurements_table(
        vertex_edges_table: dict[LidarPose, set[Edge]]
    ) -> dict[LidarPose, list[Measurement]]:
        """Creates "vertex -> measurements" table.

        Args:
            vertex_edges_table: "vertex -> edges" table.

        Returns:
            "vertex -> measurements" table.
        """

        table: dict[LidarPose, list[Measurement]] = defaultdict(list)

        for vertex, edges in vertex_edges_table.items():
            for edge in edges:
                if isinstance(edge, LidarOdometry):
                    measurement = edge.measurements[0]
                    table[vertex].append(measurement)
        return table

    @staticmethod
    def _get_unique_elements(measurements: Iterable[Measurement]) -> set[Element]:
        """Gets set of unique elements from the given collections of measurements.

        Args:
            measurements: collections of measurements.

        Returns:
            set of elements.
        """
        unique_elements = set(
            element for measurement in measurements for element in measurement.elements
        )
        return unique_elements

    @staticmethod
    def _create_vertex_elements_table(
        vertex_measurements_table: dict[LidarPose, list[Measurement]]
    ) -> dict[LidarPose, set[Element]]:
        """Creates "vertex -> elements" table.

        Args:
            vertex_measurements_table: "vertices -> measurements" table.

        Returns:
            "vertex -> elements" table.
        """

        table: dict[LidarPose, set[Element]] = defaultdict(set)

        for vertex, measurements in vertex_measurements_table.items():
            unique_elements = LidarMapFactory._get_unique_elements(measurements)
            unique_elements = {
                element for element in unique_elements if element.timestamp == vertex.timestamp
            }
            table[vertex].update(unique_elements)

        return table

    @staticmethod
    def _values_to_array(values: tuple[float, ...], num_channels: int) -> np.ndarray:
        """Converts values to pointcloud np.ndarray [num_channels, N].

        Args:
            values: values to convert.

        Returns:
            Values as array [num_channels, N].
        """
        array = np.array(values).reshape((-1, num_channels)).T
        return array

    @staticmethod
    def _filter_array(array: np.ndarray, lower_bound: float, upper_bound: float) -> np.ndarray:
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

    @staticmethod
    def _transform_pointcloud(tf1: Matrix4x4, tf2: Matrix4x4, pointcloud: np.ndarray) -> np.ndarray:
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
        pointcloud = self._values_to_array(values, self._num_channels)
        pointcloud = self._filter_array(pointcloud, self._min_range, self._max_range)
        pointcloud[3, :] = 1  # ignore intensity values
        pointcloud = self._transform_pointcloud(pose, tf, pointcloud)
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
                        pose=vertex.pose,
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
