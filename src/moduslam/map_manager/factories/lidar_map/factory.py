import logging
from typing import TypeAlias

import numpy as np
import open3d

from src.logger.logging_config import map_manager
from src.moduslam.data_manager.batch_factory.batch import Element
from src.moduslam.data_manager.batch_factory.factory import BatchFactory
from src.moduslam.frontend_manager.main_graph.graph import Graph
from src.moduslam.frontend_manager.main_graph.vertices.custom import Pose
from src.moduslam.map_manager.factories.lidar_map.config import (
    LidarPointCloudConfig,
)
from src.moduslam.map_manager.factories.lidar_map.utils import (
    create_point_cloud_from_element,
    create_pose_edges_table,
    map_elements2vertices,
)
from src.moduslam.map_manager.factories.utils import fill_elements
from src.moduslam.map_manager.maps.pointcloud import PointCloudMap
from src.moduslam.map_manager.protocols import MapFactory

logger = logging.getLogger(map_manager)

Cloud: TypeAlias = open3d.geometry.PointCloud


class LidarMapFactory(MapFactory):
    """Factory for the lidar map."""

    def __init__(self, config: LidarPointCloudConfig) -> None:
        self._map = PointCloudMap()
        self._config = config

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
        points_map = self._aggregate_point_clouds(table4, self._config)
        self._map.pointcloud = points_map

    @staticmethod
    def _aggregate_point_clouds(
        pose_elements_table: dict[Pose, list[Element]], config: LidarPointCloudConfig
    ) -> Cloud:
        """Creates and aggregates point clouds.

        Args:
            pose_elements_table: "pose -> elements" table.

        Returns:
            a 3D point cloud.

        Raises:
            TypeError: if the sensor is not of type Lidar3D.
        """
        points_map = Cloud()

        for pose, elements in pose_elements_table.items():
            pose_array = np.array(pose.value)

            for element in elements:
                cloud = create_point_cloud_from_element(element, config)
                cloud.transform(pose_array)
                points_map += cloud

        return points_map
