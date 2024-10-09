import logging

from moduslam.frontend_manager.graph_builder.builders.pointcloud_map_builder import (
    PointcloudMapBuilder,
)
from moduslam.frontend_manager.graph_builder.graph_builder_ABC import GraphBuilder
from moduslam.logger.logging_config import frontend_manager

logger = logging.getLogger(frontend_manager)


class GraphBuilderFactory:
    @staticmethod
    def create(name: str) -> type[GraphBuilder]:
        """Matches the given name with the graph builder type and returns the type of
        graph builder.

        Args:
            name: name of the graph builder to create.

        Returns:
            type of graph builder.
        """
        match name:
            case PointcloudMapBuilder.__name__:
                return PointcloudMapBuilder
            case _:
                msg = f"Graph builder of type {name!r} is not supported."
                logger.critical(msg)
                raise NotImplementedError
