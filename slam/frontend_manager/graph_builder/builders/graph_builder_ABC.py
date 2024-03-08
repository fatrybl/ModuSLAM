import logging
from abc import ABC, abstractmethod

from slam.data_manager.factory.batch import DataBatch
from slam.frontend_manager.graph.graph import Graph
from slam.frontend_manager.graph_builder.candidate_factory.graph_candidate import (
    GraphCandidate,
)

logger = logging.getLogger(__name__)


class GraphBuilder(ABC):
    """Base graph factory to create a sub-graph from the processed measurements and
    merge it with the main graph."""

    @property
    @abstractmethod
    def graph_candidate(self) -> GraphCandidate:
        """Graph candidate.

        Returns:
            (GraphCandidate): new graph candidate.
        """

    @abstractmethod
    def create_graph_candidate(self, batch: DataBatch) -> None:
        """Creates a graph candidate from the processed measurements.

        Args:
            batch (DataBatch): data batch with measurements.
        """

    @abstractmethod
    def merge(self, candidate: GraphCandidate, graph: Graph) -> None:
        """Merges the graph candidate with the graph.

        Args:
            candidate (GraphCandidate): a candidate to be merged.
            graph (Graph): main graph.
        """
