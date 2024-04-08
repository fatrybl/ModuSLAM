import logging

from slam.frontend_manager.graph_builder.builders.lidar_map_builder import (
    LidarMapBuilder,
)
from slam.frontend_manager.graph_builder.graph_builder_ABC import GraphBuilder

logger = logging.getLogger(__name__)


class GraphBuilderFactory:
    """Creates graph builder based on config."""

    @staticmethod
    def create(name: str) -> type[GraphBuilder]:
        match name:
            case LidarMapBuilder.__name__:
                return LidarMapBuilder
            case _:
                msg = f"Graph builder of type {name!r} is not supported."
                logger.critical(msg)
                raise NotImplementedError
