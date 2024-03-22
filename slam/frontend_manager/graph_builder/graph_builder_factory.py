import logging
from typing import TypeVar

from slam.frontend_manager.graph_builder.builders.graph_builder_ABC import GraphBuilder
from slam.frontend_manager.graph_builder.builders.lidar_submap_builder import (
    LidarSubMapBuilder,
)
from slam.system_configs.system.frontend_manager.graph_builder.graph_builder import (
    GraphBuilderConfig,
)

logger = logging.getLogger(__name__)

C = TypeVar("C", bound=GraphBuilderConfig)


class GraphBuilderFactory:
    """Creates graph builder based on config."""

    @staticmethod
    def create(config) -> GraphBuilder:
        match config.name:
            case LidarSubMapBuilder.__name__:
                return LidarSubMapBuilder(config)
            case _:
                msg = f"Graph builder of type {config.name!r} is not supported."
                logger.critical(msg)
                raise NotImplementedError
