import logging

from omegaconf import DictConfig

from slam.frontend_manager.graph_builder.builders.lidar_pointcloud_builder import (
    PointCloudBuilder,
)
from slam.frontend_manager.graph_builder.graph_builder_ABC import GraphBuilder

logger = logging.getLogger(__name__)


class GraphBuilderFactory:
    """
    Creates graph builder based on config.
    """

    @staticmethod
    def create(config: DictConfig) -> GraphBuilder:
        match config.type:
            case "PointCloudBuilder":
                return PointCloudBuilder(config)
            case _:
                msg = f"Graph builder type {config.type!r} is not supported."
                logger.critical(msg)
                raise NotImplementedError
