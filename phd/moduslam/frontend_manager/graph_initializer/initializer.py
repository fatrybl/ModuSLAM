import logging
from typing import Iterable

from phd.bridge.distributor import get_factory
from phd.logger.logging_config import frontend_manager
from phd.measurement_storage.measurements.base import Measurement
from phd.moduslam.frontend_manager.graph_initializer.config_factory import get_config
from phd.moduslam.frontend_manager.graph_initializer.configs import EdgeConfig
from phd.moduslam.frontend_manager.graph_initializer.distributor import (
    type_method_table,
)
from phd.moduslam.frontend_manager.main_graph.graph import Graph, GraphElement
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.utils.auxiliary_dataclasses import TimeRange

logger = logging.getLogger(frontend_manager)


class GraphInitializer:
    """Initializes the graph with prior factors."""

    def __init__(self):
        config = get_config()
        self._priors = config.values()

    def set_prior(self, graph: Graph) -> None:
        """Initializes the graph with prior factors.

        Args:
            graph: a graph to add prior factors to.
        """

        for prior in self._priors:
            item = self._create_element(graph, prior)
            if isinstance(item, Iterable):
                graph.add_elements(item)
            else:
                graph.add_element(item)

    @staticmethod
    def _create_measurement(config: EdgeConfig) -> Measurement:
        """Creates a measurement for the given configuration.

        Args:
            config: a configuration for the measurement.

        Returns:
            a new measurement.
        """
        create = type_method_table[config.vertex_type_name]
        measurement = create(config)
        return measurement

    def _create_element(self, graph: Graph, prior: EdgeConfig) -> GraphElement | list[GraphElement]:
        """Creates an edge with a prior factor.

        Args:
            graph: a graph to add prior factor(s) to.

            prior: a configuration for the edge.

        Returns:
            new graph element.
        """
        t = prior.timestamp
        measurement = self._create_measurement(prior)
        edge_factory = get_factory(type(measurement))
        clusters = {VertexCluster(): TimeRange(t, t)}
        item = edge_factory.create(graph, clusters, measurement)
        return item
