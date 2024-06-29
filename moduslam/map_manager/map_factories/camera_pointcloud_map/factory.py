import logging
from collections import deque

import numpy as np
from PIL.Image import Image

from moduslam.data_manager.batch_factory.element import Element
from moduslam.data_manager.batch_factory.factory import BatchFactory
from moduslam.frontend_manager.graph.custom_edges import VisualOdometry
from moduslam.frontend_manager.graph.custom_vertices import CameraPose
from moduslam.frontend_manager.graph.edge_storage import EdgeStorage
from moduslam.frontend_manager.graph.vertex_storage import VertexStorage
from moduslam.frontend_manager.handlers.visual_odometry.camera_features import (
    pointcloud_from_image,
)
from moduslam.logger.logging_config import map_manager
from moduslam.map_manager.map_factories.camera_pointcloud_map.utils import (
    create_vertex_elements_table,
)
from moduslam.map_manager.map_factories.utils import (
    convert_pointcloud,
    get_elements,
    transform_pointcloud,
)
from moduslam.map_manager.maps.pointcloud_map import PointcloudMap
from moduslam.setup_manager.sensors_factory.sensors import StereoCamera
from moduslam.system_configs.map_manager.map_factories.lidar_map_factory import (
    LidarMapFactoryConfig,
)
from moduslam.utils.numpy_types import Matrix3x3, Matrix4x4, Matrix4xN, MatrixNx3

logger = logging.getLogger(map_manager)


class CameraPointcloudMapFactory:
    """Factory for camera-based pointlcoud map."""

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
        """Camera-based pointcloud map."""
        return self._map

    def create(
        self, vertex_storage: VertexStorage, edge_storage: EdgeStorage, batch_factory: BatchFactory
    ) -> None:
        """Creates camera-based pointcloud map.

        Args:
            vertex_storage: storage of graph vertices.

            edge_storage: storage of graph edges.

            batch_factory: factory to create a data batch.
        """
        vertices = vertex_storage.get_vertices(CameraPose)
        edges = {edge for edge in edge_storage.edges if isinstance(edge, VisualOdometry)}
        table1 = create_vertex_elements_table(vertices, edges)
        table2 = get_elements(table1, batch_factory)
        points_map = self._create_points_map(table2)
        points_map = points_map.T
        self._map.set_points(points_map)

    @staticmethod
    def _create_pointcloud(
        pose: Matrix4x4, tf: Matrix4x4, values: tuple[Image, Image], camera_matrix: Matrix3x3
    ) -> Matrix4xN:
        """Creates a pointcloud from the given image(s) and transforms it according to
        the camera pose and base -> camera transformation.

        Args:
            pose: pose SE(3).

            tf: base -> camera transformation SE(3).

            values: stereo images.

        Returns:
            Pointcloud array [4, N].
        """
        left_image, _ = values
        pointcloud = pointcloud_from_image(left_image, camera_matrix)
        pointcloud = convert_pointcloud(pointcloud)
        result = transform_pointcloud(pose, tf, pointcloud)
        return result

    def _create_points_map(
        self, vertex_elements_table: dict[CameraPose, deque[Element]]
    ) -> MatrixNx3:
        """Creates points map from the given "vertex -> elements" table.

        Args:
            vertex_elements_table: "vertex -> elements" table.

        Returns:
            Points map array [N,3].

        Raises:
            TypeError: if the sensor is not of type StereoCamera.
        """
        pointcloud_map = np.empty(shape=(3, 0))

        for vertex, elements in vertex_elements_table.items():
            for element in elements:
                sensor = element.measurement.sensor
                values = element.measurement.values

                if isinstance(sensor, StereoCamera):
                    camera_matrix = np.array(sensor.calibrations.camera_matrix_left)

                    pointcloud = self._create_pointcloud(
                        pose=vertex.value,
                        tf=sensor.tf_base_sensor,
                        values=values,
                        camera_matrix=camera_matrix,
                    )
                    pointcloud = pointcloud[:3, :]
                    pointcloud_map = np.concatenate((pointcloud_map, pointcloud), axis=1)

                else:
                    msg = f"Sensor is of type {type(sensor).__name__!r} but not {StereoCamera.__name__!r}"
                    logger.error(msg)
                    raise TypeError(msg)

        return pointcloud_map
