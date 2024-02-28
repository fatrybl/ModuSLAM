import logging

from system_configs.system.frontend_manager.graph_builder.point_cloud_builder.config import (
    PointCloudBuilderConfig,
)

from slam.data_manager.factory.batch import DataBatch
from slam.frontend_manager.element_distributor.elements_distributor import (
    ElementDistributor,
)
from slam.frontend_manager.graph.graph import Graph
from slam.frontend_manager.graph_builder.builders.graph_builder_ABC import GraphBuilder
from slam.frontend_manager.graph_builder.candidate_factory.factory import (
    PointcloudFactory,
)
from slam.frontend_manager.graph_builder.candidate_factory.factory_ABC import (
    CandidateFactory,
)
from slam.frontend_manager.graph_builder.candidate_factory.graph_candidate import (
    GraphCandidate,
)
from slam.frontend_manager.graph_builder.graph_merger.graph_merger import GraphMerger

logger = logging.getLogger(__name__)


class PointCloudBuilder(GraphBuilder):
    """Build a graph for point-cloud based map."""

    def __init__(self, config: PointCloudBuilderConfig) -> None:
        self._distributor: ElementDistributor = ElementDistributor(config.element_distributor)
        self._candidate_factory: CandidateFactory = PointcloudFactory()
        self._merger = GraphMerger(config.graph_merger)

    @property
    def graph_candidate(self) -> GraphCandidate:
        """Graph candidate.

        Returns:
            (GraphCandidate): graph candidate.
        """
        return self._candidate_factory.graph_candidate

    def merge(self, candidate: GraphCandidate, graph: Graph) -> None:
        """Merges the candidate with the main graph.

        Args:
            candidate (GraphCandidate): a candidate to be merged.
            graph (Graph): main graph.
        """
        for state in candidate.states:
            self._merger.merge(state, graph)

    def create_graph_candidate(self, batch: DataBatch) -> None:
        """Creates graph candidate. 1) Create graph candidate. 2) Synchronize states of
        the candidate (squeeze them).

        Args:
            batch (DataBatch): data batch with measurements.
        """
        while not self._candidate_factory.candidate_ready():
            self._distributor.next_element(batch)
            self._candidate_factory.process_storage(self._distributor.storage)

        self._candidate_factory.synchronize_states()
