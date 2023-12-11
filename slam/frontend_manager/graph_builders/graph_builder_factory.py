import logging
from typing import Type

from slam.frontend_manager.graph_builders.graph_builder_ABC import GraphBuilder
from slam.frontend_manager.graph_builders.lidar_pointcloud_builder import PointCloudBuilder

logger = logging.getLogger(__name__)


class GraphBuilderFactory:

    @staticmethod
    def create(config) -> Type[GraphBuilder]:
        if config.type == 'PointCloudBuilder':
            return PointCloudBuilder(config)
        else:
            raise NotImplementedError
