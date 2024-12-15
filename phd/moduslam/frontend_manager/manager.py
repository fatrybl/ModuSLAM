import logging

from phd.external.handlers_factory.factory import Factory
from phd.logger.logging_config import frontend_manager
from phd.moduslam.data_manager.batch_factory.batch import DataBatch
from phd.moduslam.frontend_manager.graph_builders.suboptimal_builder import Builder
from phd.moduslam.frontend_manager.graph_initializer.initializer import GraphInitializer
from phd.moduslam.frontend_manager.main_graph.graph import Graph

logger = logging.getLogger(frontend_manager)


class FrontendManager:
    """Manager for suboptimal graph construction."""

    def __init__(self):
        Factory.init_handlers()
        handlers = Factory.get_handlers()
        self._graph = Graph()
        self._builder = Builder(handlers)
        self._initializer = GraphInitializer()
        logger.debug("Frontend Manager has been configured.")

    @property
    def graph(self) -> Graph:
        """Main graph."""
        return self._graph

    @graph.setter
    def graph(self, graph: Graph) -> None:
        """Sets main graph."""
        self._graph = graph

    def set_prior(self) -> None:
        """Adds prior factors to the graph."""
        self._initializer.set_prior(self._graph)
        logger.debug("Prior factors have been added.")

    def create_graph(self, batch: DataBatch) -> None:
        """Creates main graph by merging sub-graphs (graph candidates).

        Args:
            batch: data batch with elements.
        """
        self._graph = self._builder.create_graph(self._graph, batch)
