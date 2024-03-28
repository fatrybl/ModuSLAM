import logging
from abc import ABC, abstractmethod

from slam.data_manager.factory.batch import DataBatch
from slam.frontend_manager.graph.graph import Graph
from slam.frontend_manager.graph_builder.candidate_factory.graph_candidate import (
    GraphCandidate,
)
from slam.system_configs.system.frontend_manager.graph_builder.graph_builder import (
    GraphBuilderConfig,
)

logger = logging.getLogger(__name__)


class GraphBuilder(ABC):
    """Base graph factory to create a sub-graph from the processed measurements and
    merge it with the main graph."""

    @abstractmethod
    def __init__(self, config: GraphBuilderConfig) -> None:
        pass

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
    def merge_graph_candidate(self, graph: Graph) -> None:
        """Merges the graph candidate with the graph.

        Args:
            graph (Graph): a graph to be merged with.
        """

    @abstractmethod
    def clear_candidate(self) -> None:
        """Clears the graph candidate."""
