import logging
from collections import deque

import numpy as np
from PIL.Image import Image

from phd.logger.logging_config import map_manager
from phd.moduslam.custom_types.aliases import Matrix4x4
from phd.moduslam.custom_types.numpy import Matrix3x3, Matrix4xN, MatrixNx3
from phd.moduslam.data_manager.batch_factory.batch import Element
from phd.moduslam.data_manager.batch_factory.factory import BatchFactory
from phd.moduslam.frontend_manager.main_graph.graph import Graph
from phd.moduslam.frontend_manager.main_graph.vertices.custom import Pose
from phd.moduslam.map_manager.map_factories.camera_pointcloud.depth_estimator import (
    DepthEstimator,
)
from phd.moduslam.map_manager.map_factories.camera_pointcloud.utils import (
    pointcloud_from_image,
)
from phd.moduslam.map_manager.map_factories.utils import (
    convert_pointcloud,
    transform_pointcloud,
)
from phd.moduslam.map_manager.maps.pointcloud import PointCloudMap
from phd.moduslam.setup_manager.sensors_factory.sensors import StereoCamera

logger = logging.getLogger(map_manager)


class CameraPointcloudMapFactory:
    """Factory for camera-based pointlcoud map."""

    def __init__(self) -> None:
        """
        Args:
            config: configuration of the factory.
        """
        self._map = PointCloudMap()
        self._depth_estimator = DepthEstimator()
        # self._num_channels: int = config.num_channels
        # self._min_range: float = config.min_range
        # self._max_range: float = config.max_range

    @property
    def map(self) -> PointCloudMap:
        """Camera-based pointcloud map."""
        return self._map

    def create(self, graph: Graph, batch_factory: BatchFactory) -> None:
        """Creates camera-based point cloud map.

        Args:
            graph: graph to create the map from.

            batch_factory: factory to create a data batch.
        """
        raise NotImplementedError

    def _create_pointcloud(
        self,
        pose: Matrix4x4,
        tf: Matrix4x4,
        values: tuple[Image, Image],
        camera_matrix: Matrix3x3,
    ) -> Matrix4xN:
        """Creates a point cloud from the given image(s) and transforms it according to
        the camera pose and base -> camera transformation.

        Args:
            pose: pose SE(3).

            tf: base -> camera transformation SE(3).

            values: stereo images.

        Returns:
            Pointcloud array [4, N].
        """
        pose_array = np.array(pose)
        tf_array = np.array(tf)
        left_image, _ = values
        depth_image = self._depth_estimator.estimate_depth(left_image)
        pointcloud = pointcloud_from_image(depth_image, camera_matrix)
        pointcloud = convert_pointcloud(pointcloud)
        result = transform_pointcloud(pose_array, tf_array, pointcloud)
        return result

    def _create_points_map(self, vertex_elements_table: dict[Pose, deque[Element]]) -> MatrixNx3:
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
                        vertex.value,
                        sensor.tf_base_sensor,
                        values,
                        camera_matrix,
                    )
                    pointcloud = pointcloud[:3, :]
                    pointcloud_map = np.concatenate((pointcloud_map, pointcloud), axis=1)

                else:
                    msg = f"Sensor is of type {type(sensor).__name__!r} but not {StereoCamera.__name__!r}"
                    logger.error(msg)
                    raise TypeError(msg)

        return pointcloud_map
