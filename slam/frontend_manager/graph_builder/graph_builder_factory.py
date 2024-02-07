import logging
from typing import TypeVar

from configs.system.frontend_manager.graph_builder.graph_builder import (
    GraphBuilderConfig,
)
from slam.frontend_manager.graph_builder.builders.lidar_pointcloud_builder import (
    PointCloudBuilder,
)
from slam.frontend_manager.graph_builder.graph_builder_ABC import GraphBuilder

logger = logging.getLogger(__name__)

C = TypeVar("C", bound=GraphBuilderConfig)


class GraphBuilderFactory:
    """
    Creates graph builder based on config.
    """

    @staticmethod
    def create(config) -> GraphBuilder:
        match config.class_name:
            case PointCloudBuilder.__name__:
                return PointCloudBuilder(config)
            case _:
                msg = f"Graph builder type {config.class_name!r} is not supported."
                logger.critical(msg)
                raise NotImplementedError
