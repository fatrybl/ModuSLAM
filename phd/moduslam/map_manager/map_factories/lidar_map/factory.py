import logging

import numpy as np

from phd.logger.logging_config import map_manager
from phd.moduslam.custom_types.aliases import Matrix4x4
from phd.moduslam.custom_types.numpy import MatrixNx3
from phd.moduslam.data_manager.batch_factory.batch import Element
from phd.moduslam.data_manager.batch_factory.factory import BatchFactory
from phd.moduslam.frontend_manager.main_graph.graph import Graph
from phd.moduslam.frontend_manager.main_graph.vertices.custom import Pose
from phd.moduslam.map_manager.map_factories.lidar_map.config import (
    LidarPointCloudConfig,
)
from phd.moduslam.map_manager.map_factories.lidar_map.utils import (
    create_pose_edges_table,
    map_elements2vertices,
    values_to_array,
)
from phd.moduslam.map_manager.map_factories.utils import (
    fill_elements,
    filter_array,
    transform_pointcloud,
)
from phd.moduslam.map_manager.maps.pointcloud import PointCloudMap
from phd.moduslam.map_manager.protocols import MapFactory
from phd.moduslam.sensors_factory.sensors import Lidar3D

logger = logging.getLogger(map_manager)


class LidarMapFactory(MapFactory):
    """Factory for the lidar map."""

    def __init__(self, config: LidarPointCloudConfig) -> None:
        self._map = PointCloudMap()
        self._num_channels = config.num_channels
        self._min_range = config.min_range
        self._max_range = config.max_range

    @property
    def map(self) -> PointCloudMap:
        """Lidar point cloud map instance."""
        return self._map

    def create_map(self, graph: Graph, batch_factory: BatchFactory) -> None:
        """Creates a lidar point cloud map.

        Args:
            graph: graph to create a map from.

            batch_factory: factory to create a data batch.
        """
        poses = graph.vertex_storage.get_vertices(Pose)
        table1 = {p: graph.connections[p] for p in poses}
        table2 = create_pose_edges_table(table1)
        table3 = map_elements2vertices(table2)
        table4 = fill_elements(table3, batch_factory)
        points_map = self._create_points_map(table4)
        self._map.set_points(points_map)

    def _create_points_map(self, pose_elements_table: dict[Pose, list[Element]]) -> MatrixNx3:
        """Creates a points map from the given "vertex -> elements" table.

        Args:
            pose_elements_table: "pose -> elements" table.

        Returns:
            Points map array [N,3].

        Raises:
            TypeError: if the sensor is not of type Lidar3D.
        """
        pointcloud_map = np.empty(shape=(0, 4))

        for pose, elements in pose_elements_table.items():
            for element in elements:
                pointcloud = self._get_cloud(pose.value, element)
                pointcloud_map = np.vstack((pointcloud_map, pointcloud))

        pointcloud_map = pointcloud_map[:, :3]  # ignore intensity values.
        return pointcloud_map

    def _get_cloud(self, pose: Matrix4x4, element: Element) -> np.ndarray:
        sensor = element.measurement.sensor
        values = element.measurement.values

        if isinstance(sensor, Lidar3D):
            tf = sensor.tf_base_sensor
            pointcloud = self._create_pointcloud(pose, tf, values)
            return pointcloud

        else:
            msg = f"Sensor is of type {type(sensor).__name__!r} but not {Lidar3D.__name__!r}"
            logger.error(msg)
            raise TypeError(msg)

    def _create_pointcloud(
        self, pose: Matrix4x4, tf: Matrix4x4, values: tuple[float, ...]
    ) -> np.ndarray:
        """Creates a point cloud in global coordinate system by applying
        transformations. Ignores intensity values.

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
        pointcloud[:, 3] = 1  # ignore intensity channel and make SE(3) compatible.
        pointcloud = filter_array(pointcloud, self._min_range, self._max_range)
        pointcloud = transform_pointcloud(pose_array, tf_array, pointcloud)
        return pointcloud
