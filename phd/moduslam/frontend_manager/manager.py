import logging

from phd.external.handlers_factory.factory import Factory
from phd.logger.logging_config import frontend_manager
from phd.measurement_storage.measurements.base import Measurement
from phd.moduslam.data_manager.batch_factory.batch import DataBatch
from phd.moduslam.frontend_manager.graph_builders.suboptimal_builder import Builder
from phd.moduslam.frontend_manager.graph_initializer.config_factory import get_config
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
        logger.debug("Frontend Manager has been configured.")

    @property
    def graph(self) -> Graph:
        """Main graph."""
        return self._graph

    @staticmethod
    def create_prior_measurements() -> list[Measurement]:
        """Create prior measurements.

        Returns:
            prior measurements.
        """
        config = get_config()
        priors = config.values()
        measurements = GraphInitializer.create_measurements(priors)
        return measurements

    def create_graph(self, batch: DataBatch) -> None:
        """Creates main graph by merging sub-graphs (graph candidates).

        Args:
            batch: data batch with elements.
        """
        self._graph = self._builder.create_graph(self._graph, batch)
