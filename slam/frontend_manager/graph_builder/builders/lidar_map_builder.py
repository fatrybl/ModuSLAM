import logging
from typing import Generic

from slam.data_manager.factory.batch import DataBatch
from slam.frontend_manager.elements_distributor import ElementDistributor
from slam.frontend_manager.graph.base_edges import GraphEdge
from slam.frontend_manager.graph.base_vertices import GraphVertex
from slam.frontend_manager.graph.graph import Graph
from slam.frontend_manager.graph_builder.candidate_factory.factories.factory_ABC import (
    CandidateFactory,
)
from slam.frontend_manager.graph_builder.candidate_factory.factories.lidar_submap import (
    LidarMapCandidateFactory,
)
from slam.frontend_manager.graph_builder.candidate_factory.graph_candidate import (
    GraphCandidate,
)
from slam.frontend_manager.graph_builder.graph_builder_ABC import GraphBuilder
from slam.frontend_manager.graph_builder.graph_merger import GraphMerger
from slam.logger.logging_config import frontend_manager
from slam.system_configs.frontend_manager.graph_builder.graph_builder import (
    GraphBuilderConfig,
)

logger = logging.getLogger(frontend_manager)


class LidarMapBuilder(GraphBuilder, Generic[GraphVertex, GraphEdge]):
    """Builds a graph for point-cloud based map."""

    def __init__(self, config: GraphBuilderConfig) -> None:
        super().__init__(config)
        self._distributor: ElementDistributor = ElementDistributor()
        self._candidate_factory: CandidateFactory = LidarMapCandidateFactory()
        self._merger = GraphMerger[GraphVertex, GraphEdge]()
        self._merger.init_table(config.graph_merger.handler_edge_factory_table)
        self._distributor.init_table(config.element_distributor.sensor_handlers_table)
        self._candidate_factory.init_table(config.candidate_factory.handler_state_analyzer_table)

    @property
    def graph_candidate(self) -> GraphCandidate:
        """Graph candidate to be merged with the graph."""
        return self._candidate_factory.graph_candidate

    def create_graph_candidate(self, data_batch: DataBatch) -> None:
        """Creates graph candidate.

        Args:
            data_batch: a data batch with measurements.
        """
        while not self._candidate_factory.candidate_ready() and not data_batch.empty:
            element = data_batch.first
            self._distributor.distribute_element(element)
            self._candidate_factory.process_storage(self._distributor.storage)
            data_batch.remove_first()

    def merge_graph_candidate(self, graph: Graph) -> None:
        """Merges the graph candidate with the graph.

        Args:
            graph: a graph to be merged with.
        """
        if self._candidate_factory.candidate_ready():
            for state in self.graph_candidate.states:
                self._merger.merge(state, graph)
        else:
            logger.info("No candidate to merge")

    def clear_candidate(self) -> None:
        """Clears the graph candidate."""

        if self._candidate_factory.candidate_ready():
            for state in self.graph_candidate.states:
                measurements = state.data.values()
                self._distributor.clear_storage(measurements)

            self.graph_candidate.clear()

        else:
            logger.info("No candidate to clear")
