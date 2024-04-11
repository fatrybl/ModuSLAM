import logging
from collections import defaultdict, deque
from collections.abc import Iterable

import numpy as np

from slam.data_manager.factory.batch_factory import BatchFactory
from slam.data_manager.factory.element import Element
from slam.frontend_manager.element_distributor.measurement_storage import Measurement
from slam.frontend_manager.graph.base_edges import Edge
from slam.frontend_manager.graph.base_vertices import Vertex
from slam.frontend_manager.graph.custom_edges import LidarOdometry
from slam.frontend_manager.graph.custom_vertices import LidarPose
from slam.frontend_manager.graph.vertex_storage import VertexStorage
from slam.map_manager.maps.lidar_map import LidarMap
from slam.utils.deque_set import DequeSet

logger = logging.getLogger(__name__)


class LidarMapFactory:
    """Class to create a lidar map."""

    def __init__(self) -> None:
        self._map = LidarMap()
        self._required_vertex_type = LidarPose

    @property
    def map(self) -> LidarMap:
        """Lidar map.

        Returns:
            (LidarMap): map instance.
        """
        return self._map

    @property
    def vertices_types(self) -> tuple[type[Vertex]]:
        """Required vertices types to create a map.

        Returns:
            (tuple[type[Vertex]]): vertices types.
        """
        return (self._required_vertex_type,)

    def create(self, vertex_storage: VertexStorage, batch_factory: BatchFactory) -> None:
        """Creates a Lidar Map.

        Args:
            vertex_storage (VertexStorage): storage of the vertices.
            batch_factory (BatchFactory): factory to create a batch.
        """
        table = self._create_requests_table(vertex_storage)
        table_with_data = self._get_elements(table, batch_factory)
        pcd_data = self._get_pointcloud(table_with_data)
        self._map.set_pointcloud(pcd_data)

    def _create_requests_table(
        self, vertex_storage: VertexStorage
    ) -> dict[LidarPose, list[Element]]:
        """
        Creates a table of vertices and their elements.
        Args:
            vertex_storage:

        Returns:

        """
        vertices: DequeSet[LidarPose] = vertex_storage.get_vertices(self._required_vertex_type)
        vertex_edges_table: dict[LidarPose, set[Edge]] = {v: v.edges for v in vertices}
        vertex_measurements_table = self._create_vertex_measurements_table(vertex_edges_table)
        vertex_elements_table = self._create_vertex_elements_table(vertex_measurements_table)
        return vertex_elements_table

    @staticmethod
    def _get_elements(
        vertex_elements_table: dict[LidarPose, list[Element]], batch_factory: BatchFactory
    ) -> dict[LidarPose, deque[Element]]:
        """Gets elements with raw lidar measurements and assign to the corresponding
        vertices of the given table.

        Args:
            vertex_elements_table (dict[Vertex, set[Element]]): table of vertices and their elements
                                                                without raw lidar measurements.
            batch_factory (BatchFactory): factory to create a batch.

        Returns:
            dict[Vertex, deque[Element]]: table of vertices and their elements with raw lidar measurements.
        """
        table: dict[LidarPose, deque[Element]] = defaultdict(deque)
        for vertex, elements in vertex_elements_table.items():
            batch_factory.create_batch(elements)
            table[vertex] = batch_factory.batch.data

        return table

    @staticmethod
    def _create_vertex_measurements_table(
        vertex_edges_table: dict[LidarPose, set[Edge]]
    ) -> dict[LidarPose, list[Measurement]]:
        """Creates a table of vertices and their measurements.

        Args:
            vertex_edges_table (dict[LidarPose, set[Edge]]): table of vertices and their edges.

        Returns:
            dict[LidarPose, list[Measurement]]: table of vertices and their measurements.
        """

        table: dict[LidarPose, list[Measurement]] = defaultdict(list)

        for vertex, edges in vertex_edges_table.items():
            for edge in edges:
                if isinstance(edge, LidarOdometry):
                    measurement = edge.measurements[0]
                    table[vertex].append(measurement)
        return table

    @staticmethod
    def _create_vertex_elements_table(
        vertex_measurements_table: dict[LidarPose, list[Measurement]]
    ) -> dict[LidarPose, list[Element]]:
        """Creates a table of vertices and their elements.

        Args:
            vertex_measurements_table (dict[LidarPose, list[Measurement]]): table of vertices and their measurements.

        Returns:
            dict[Vertex, list[Element]]: table of vertices and their elements.
        """

        table: dict[LidarPose, list[Element]] = defaultdict(list)

        for vertex, measurements in vertex_measurements_table.items():
            set_of_elements = set([el for m in measurements for el in m.elements])
            list_of_elements = [
                element for element in set_of_elements if element.timestamp == vertex.timestamp
            ]
            table[vertex].extend(list_of_elements)

        return table

    @staticmethod
    def _elements_to_pointcloud(elements: Iterable[Element]) -> np.ndarray:
        """Converts elements` values to pointcloud.

        Args:
            elements (Iterable[Element]): elements to convert.

        Returns:
            (np.ndarray[4xN]): array with the pointcloud.
        """

        points: list[float] = []
        for element in elements:
            points.extend(element.measurement.values)

        pointcloud = np.array(points)
        pointcloud = pointcloud.reshape((-1, 4))
        pointcloud[:, 3] = (
            1  # ignore intensity information and make suitable for matrix multiplications
        )

        pointcloud = pointcloud.T
        return pointcloud

    @staticmethod
    def filter_array(arr, lower_bound, upper_bound):
        mask = np.any((arr[:3, :] >= lower_bound) & (arr[:3, :] <= upper_bound), axis=0)
        filtered_arr = arr[:, mask]
        return filtered_arr

    @staticmethod
    def _transform_pointcloud(vertex: LidarPose, pointcloud: np.ndarray) -> np.ndarray:
        """Transforms points` coordinates  according to the given vertex pose.

        Args:
            vertex (LidarPose): vertex with the pose.
            pointcloud (np.ndarray[4xN]): pointcloud to transform.

        Returns:
            (np.ndarray): transformed pointcloud.
        """
        extrinsic: np.ndarray = np.array(
            [
                [-0.514521, 0.701075, -0.493723, -0.333596],
                [-0.492472, -0.712956, -0.499164, -0.373928],
                [-0.701954, -0.0136853, 0.712091, 1.94377],
                [0, 0, 0, 1],
            ]
        )
        pose = vertex.SE3
        return pose @ extrinsic @ pointcloud

    def _get_pointcloud(self, vertex_elements_table: dict[LidarPose, deque[Element]]) -> np.ndarray:
        """Converts elements to pointclouds and transforms them according to the vertex
        pose.

        Args:
            vertex_elements_table (dict[LidarPose, deque[Element]]): table of vertices and their elements.

        Returns:
            (np.ndarray[Nx4]): array with the pointcloud.
        """
        pointcloud_map = np.empty((4, 0))

        for vertex, elements in vertex_elements_table.items():
            pointcloud = self._elements_to_pointcloud(elements)
            pointcloud = self.filter_array(pointcloud, 5, 100)
            pointcloud = self._transform_pointcloud(vertex, pointcloud)
            pointcloud_map = np.concatenate((pointcloud_map, pointcloud), axis=1)

        pointcloud_map = pointcloud_map[:3, :].T  # ignore the last row with ones
        return pointcloud_map
