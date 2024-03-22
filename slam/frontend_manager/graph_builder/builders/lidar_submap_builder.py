import logging

from slam.data_manager.factory.batch import DataBatch
from slam.frontend_manager.element_distributor.elements_distributor import (
    ElementDistributor,
)
from slam.frontend_manager.graph.graph import Graph
from slam.frontend_manager.graph_builder.builders.graph_builder_ABC import GraphBuilder
from slam.frontend_manager.graph_builder.candidate_factory.factories.lidar_submap import (
    LidarSubmapCandidateFactory,
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


class LidarSubMapBuilder(GraphBuilder):
    """Builds a graph for point-cloud based map."""

    def __init__(self, config: GraphBuilderConfig) -> None:
        self._distributor: ElementDistributor = ElementDistributor(config.element_distributor)
        self._candidate_factory: CandidateFactory = LidarSubmapCandidateFactory()
        self._merger = GraphMerger(config.graph_merger)

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

        for state in self.graph_candidate.states:
            self._merger.merge(state, graph)

    def create_graph_candidate(self, batch: DataBatch) -> None:
        """Creates graph candidate. 1) Create graph candidate. 2) Synchronize states of
        the candidate (Optional).

        Args:
            batch (DataBatch): data batch with measurements.
        """
        while not self._candidate_factory.candidate_ready():
            self._distributor.next_element(batch)
            self._candidate_factory.process_storage(self._distributor.storage)

        self._candidate_factory.synchronize_states()

    def clear_candidate(self) -> None:
        """
        Clears the graph candidate:
            1) Removes measurements of each state from the storage.
            2) Removes measurements of each state in the graph candidate.
        """
        for state in self.graph_candidate.states:
            measurements = state.data.values()
            self._distributor.clear_storage(measurements)

        self.graph_candidate.clear()
