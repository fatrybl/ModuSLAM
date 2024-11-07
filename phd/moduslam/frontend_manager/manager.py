import logging

from moduslam.data_manager.batch_factory.batch import DataBatch
from moduslam.logger.logging_config import frontend_manager
from phd.moduslam.frontend_manager.base_config import FrontendManagerConfig
from phd.moduslam.frontend_manager.graph_builders.suboptimal_builder import Builder
from phd.moduslam.frontend_manager.graph_initializer.initializer import GraphInitializer
from phd.moduslam.frontend_manager.main_graph.graph import Graph

logger = logging.getLogger(frontend_manager)


class FrontendManager:
    """Manager for suboptimal graph construction."""

    def __init__(self, config: FrontendManagerConfig):
        """
        Args:
            config: frontend manager configuration.
        """
        self._graph: Graph = Graph()
        self._builder = Builder(config.handlers)
        self._initializer = GraphInitializer(config.graph_initializer)
        logger.debug("Frontend Manager has been configured.")

    @property
    def graph(self) -> Graph:
        """Main graph."""
        return self._graph

    def set_prior(self) -> None:
        """Sets prior factors to the graph."""
        self._initializer.set_prior(self._graph)
        logger.debug("Prior factors have been added.")

    def create_graph(self, batch: DataBatch) -> None:
        """Creates main graph by merging sub-graphs (graph candidates).

        Args:
            batch: data batch with elements.
        """

        new_elements = self._builder.create_elements(batch, self._graph)
        for element in new_elements:
            self._graph.add_element(element)
