import logging

from omegaconf import DictConfig

from slam.data_manager.factory.batch import DataBatch
from slam.frontend_manager.elements_distributor.elements_distributor import (
    ElementDistributor,
)
from slam.frontend_manager.graph.graph import Graph
from slam.frontend_manager.graph_builder.candidate_factory.factory import (
    PointcloudFactory,
)
from slam.frontend_manager.graph_builder.candidate_factory.factory_ABC import (
    CandidateFactory,
)
from slam.frontend_manager.graph_builder.candidate_factory.graph_candidate import (
    GraphCandidate,
)
from slam.frontend_manager.graph_builder.graph_builder_ABC import GraphBuilder
from slam.frontend_manager.graph_builder.graph_merger.graph_merger import GraphMerger

logger = logging.getLogger(__name__)


class PointCloudBuilder(GraphBuilder):
    """
    Build a graph for point-cloud based map.
    """

    def __init__(self, config: DictConfig) -> None:
        self._distributor: ElementDistributor = ElementDistributor(config.element_distributor)
        self._candidate_factory: CandidateFactory = PointcloudFactory()
        self._merger = GraphMerger()

    @property
    def graph_candidate(self) -> GraphCandidate:
        """
        Graph candidate.
        Returns:
            (GraphCandidate): graph candidate.
        """
        return self._candidate_factory.graph_candidate

    def merge(self, candidate: GraphCandidate, graph: Graph) -> None:
        """
        Merges the candidate with the main graph.

        Args:
            candidate (GraphCandidate): a candidate to be merged.
            graph (Graph): main graph.
        """
        for state in candidate.states:
            self._merger.merge(state, graph)

    def create_graph_candidate(self, batch: DataBatch) -> None:
        """
        Creates graph candidate.

        Args:
            batch (DataBatch): data batch with measurements.
        """
        while not self._candidate_factory.candidate_ready():
            self._distributor.next_element(batch)
            self._candidate_factory.process_storage(self._distributor.storage)

        self._candidate_factory.synchronize_states()
