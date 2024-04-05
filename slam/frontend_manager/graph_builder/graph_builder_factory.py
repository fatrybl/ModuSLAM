import logging

from slam.frontend_manager.graph_builder.builders.lidar_submap_builder import (
    LidarMapBuilder,
)
from slam.frontend_manager.graph_builder.graph_builder_ABC import GraphBuilder

logger = logging.getLogger(__name__)


class GraphBuilderFactory:
    """Creates graph builder based on config."""

    @staticmethod
    def create(config) -> GraphBuilder:
        match config.name:
            case LidarMapBuilder.__name__:
                return LidarMapBuilder(config)
            case _:
                msg = f"Graph builder of type {config.name!r} is not supported."
                logger.critical(msg)
                raise NotImplementedError
