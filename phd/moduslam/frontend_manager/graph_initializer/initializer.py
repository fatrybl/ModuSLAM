import logging
from typing import Iterable, cast

from hydra import compose, initialize
from hydra.core.config_store import ConfigStore

from phd.bridge.distributor import get_factory
from phd.logger.logging_config import frontend_manager
from phd.measurements.processed import Measurement
from phd.moduslam.frontend_manager.graph_initializer.config_objects import (
    EdgeConfig,
    InitializerConfig,
    PriorLinearVelocity,
    PriorPose,
)
from phd.moduslam.frontend_manager.graph_initializer.distributor import (
    type_method_table,
)
from phd.moduslam.frontend_manager.main_graph.graph import Graph, GraphElement
from phd.moduslam.frontend_manager.main_graph.vertex_storage.cluster import (
    VertexCluster,
)
from phd.moduslam.utils.auxiliary_dataclasses import TimeRange

logger = logging.getLogger(frontend_manager)


def register_configs():
    cs = ConfigStore.instance()
    cs.store(name="base_initializer", node=InitializerConfig)
    cs.store(name="base_pose", node=PriorPose)
    cs.store(name="base_linear_velocity", node=PriorLinearVelocity)


register_configs()


class GraphInitializer:
    """Initializes the graph with prior factors."""

    def __init__(self):
        with initialize(version_base=None, config_path="configs"):
            cfg = compose(config_name="config")
            config = cast(InitializerConfig, cfg)  # avoid MyPy warnings
            self._priors = config.priors.values()

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
