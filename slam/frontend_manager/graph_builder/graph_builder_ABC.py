import logging
from abc import ABC, abstractmethod

from slam.data_manager.factory.batch import DataBatch
from slam.frontend_manager.graph.graph import Graph
from slam.frontend_manager.graph_builder.candidate_factory.graph_candidate import (
    GraphCandidate,
)
from slam.system_configs.frontend_manager.graph_builder.graph_builder import (
    GraphBuilderConfig,
)

logger = logging.getLogger(__name__)


class GraphBuilder(ABC):
    """Base abstract graph builder.

    Creates a sub-graph from the measurements and merges it with the main graph.
    """

    @abstractmethod
    def __init__(self, config: GraphBuilderConfig) -> None:
        """
        Args:
            config: a configuration for the graph builder.
        """

    @property
    @abstractmethod
    def graph_candidate(self) -> GraphCandidate:
        """Graph candidate."""

    @abstractmethod
    def create_graph_candidate(self, batch: DataBatch) -> None:
        """Creates graph candidate. Uses the measurements from the data batch.

        Args:
            batch: a data batch with measurements.
        """

    @abstractmethod
    def merge_graph_candidate(self, graph: Graph) -> None:
        """Merges the graph candidate with the given graph.

        Args:
            graph: a graph to be merged with.
        """

    @abstractmethod
    def clear_candidate(self) -> None:
        """Clears the graph candidate."""
