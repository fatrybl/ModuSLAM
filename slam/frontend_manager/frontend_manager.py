import logging

from configs.system.frontend_manager.frontend_manager import FrontendManagerConfig
from slam.data_manager.factory.batch import DataBatch
from slam.frontend_manager.elements_distributor.elements_distributor import (
    ElementDistributor,
)
from slam.frontend_manager.graph.graph import Graph
from slam.frontend_manager.graph.graph_candidate import GraphCandidate
from slam.frontend_manager.graph_builders.candidate_factory.candidate_factory import (
    CandidateFactory,
)
from slam.frontend_manager.graph_builders.graph_builder_ABC import GraphBuilder
from slam.frontend_manager.graph_builders.graph_builder_factory import (
    GraphBuilderFactory,
)
from slam.frontend_manager.graph_builders.graph_merger.graph_merger import GraphMerger

logger = logging.getLogger(__name__)


class FrontendManager:
    """
    Manages all frontend procedures: process measurements, build graph, detect loops and anomalies...
    """

    def __init__(self, config: FrontendManagerConfig):
        self.graph: Graph = Graph()
        self.graph_builder: GraphBuilder = GraphBuilderFactory.create(config.graph_builder)
        self.distributor: ElementDistributor = ElementDistributor()

    def _create_graph_candidate(self, batch: DataBatch) -> None:
        """
        Creates graph candidate.

        Args:
            batch (DataBatch): data batch to be used for graph candidate construction.
        """
        while not self.graph_builder.graph_candidate_ready():
            self.distributor.next_element(batch)
            self.graph_builder.process_storage(self.distributor.storage)

    def _merge(self) -> None:
        """
        Connects a graph candidate with the main graph.
        """
        factory: CandidateFactory = self.graph_builder.candidate_factory
        candidate: GraphCandidate = factory.graph_candidate
        merger: GraphMerger = self.graph_builder.candidate_merger
        merger.connect(self.graph, candidate)

    def create_graph(self, batch: DataBatch) -> None:
        """
        Creates main graph by merging sub-graphs.

        Args:
            batch (DataBatch): data batch with elements.
        """
        self._create_graph_candidate(batch)
        self._merge()
