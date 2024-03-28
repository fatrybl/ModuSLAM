import logging
from typing import TypeVar

from slam.frontend_manager.graph_builder.builders.graph_builder_ABC import GraphBuilder
from slam.frontend_manager.graph_builder.builders.lidar_submap_builder import (
    LidarMapBuilder,
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
            case LidarMapBuilder.__name__:
                return LidarMapBuilder(config)
            case _:
                msg = f"Graph builder of type {config.name!r} is not supported."
                logger.critical(msg)
                raise NotImplementedError
