import logging

from moduslam.logger.logging_config import frontend_manager
from phd.moduslam.frontend_manager.graph_initializer.config import (
    GraphInitializerConfig,
    PriorConfig,
)
from phd.moduslam.frontend_manager.main_graph.graph import Graph
from phd.moduslam.frontend_manager.main_graph.objects import GraphElement

logger = logging.getLogger(frontend_manager)

FAKE_SENSOR_NAME = "Prior sensor"


class GraphInitializer:
    """Initializes the graph with prior factors."""

    def __init__(self, config: GraphInitializerConfig):
        """
        Args:
            config: graph initializer configuration.
        """
        self._priors = config.priors.values()

    def set_prior(self, graph: Graph) -> None:
        """Initializes the graph with prior factors.

        Args:
            graph: a graph to add prior factors to.
        """

        for prior in self._priors:
            element = self._create_element(graph, prior)
            graph.add_element(element)

    def _create_element(self, graph: Graph, prior: PriorConfig) -> GraphElement:
        """Creates an edge with a prior factor.

        Args:
            graph: a graph to add the edge at.

            prior: a prior configuration.

        Returns:
            list with 1 edge.
        """

        # measurement = self._init_measurement(
        #     prior.measurement,
        #     prior.measurement_noise_covariance,
        #     prior.timestamp,
        #     prior.file_path,
        # )
        # edge_factory = self._get_edge_factory(prior.edge_factory_name)
        # edge = edge_factory.create(
        #     graph=graph,
        #     measurements=OrderedSet((measurement,)),
        #     timestamp=prior.timestamp,
        # )
        # return edge
        raise NotImplementedError
