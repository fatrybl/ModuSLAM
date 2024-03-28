import logging
from typing import Generic

from slam.data_manager.factory.batch import DataBatch
from slam.frontend_manager.element_distributor.elements_distributor import (
    ElementDistributor,
)
from slam.frontend_manager.graph.base_edges import GraphEdge
from slam.frontend_manager.graph.graph import Graph
from slam.frontend_manager.graph.vertices import GraphVertex
from slam.frontend_manager.graph_builder.builders.graph_builder_ABC import GraphBuilder
from slam.frontend_manager.graph_builder.candidate_factory.factories.lidar_submap import (
    LidarMapCandidateFactory,
)
from slam.frontend_manager.graph_builder.candidate_factory.factory_ABC import (
    CandidateFactory,
)
from slam.frontend_manager.graph_builder.candidate_factory.graph_candidate import (
    GraphCandidate,
)
from slam.frontend_manager.graph_builder.graph_merger import GraphMerger
from slam.system_configs.system.frontend_manager.graph_builder.graph_builder import (
    GraphBuilderConfig,
)

logger = logging.getLogger(__name__)


class LidarMapBuilder(GraphBuilder, Generic[GraphVertex, GraphEdge]):
    """Builds a graph for point-cloud based map."""

    def __init__(self, config: GraphBuilderConfig) -> None:
        self._distributor: ElementDistributor = ElementDistributor(config.element_distributor)
        self._candidate_factory: CandidateFactory = LidarMapCandidateFactory(
            config.candidate_factory
        )
        self._merger = GraphMerger[GraphVertex, GraphEdge](config.graph_merger)

    @property
    def graph_candidate(self) -> GraphCandidate:
        """Graph candidate.

        Returns:
            (GraphCandidate): graph candidate.
        """
        return self._candidate_factory.graph_candidate

    def merge_graph_candidate(self, graph: Graph) -> None:
        """Merges the graph candidate with the graph.

        Args:
            graph (Graph): a graph to be merged with.
        """
        if self._candidate_factory.candidate_ready():
            for state in self.graph_candidate.states:
                self._merger.merge(state, graph)
        else:
            logger.info("No candidate to merge")

    def create_graph_candidate(self, batch: DataBatch) -> None:
        """Creates graph candidate.

        Args:
            batch (DataBatch): data batch with measurements.
        """
        while not self._candidate_factory.candidate_ready() and not batch.empty():
            self._distributor.next_element(batch)
            self._candidate_factory.process_storage(self._distributor.storage)
            batch.remove_first()

    def clear_candidate(self) -> None:
        """Clears the graph candidate."""

        if self._candidate_factory.candidate_ready():
            for state in self.graph_candidate.states:
                measurements = state.data.values()
                self._distributor.clear_storage(measurements)

            self.graph_candidate.clear()
