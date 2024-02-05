import logging

from omegaconf import DictConfig

from slam.data_manager.factory.batch import DataBatch
from slam.frontend_manager.graph.graph import Graph
from slam.frontend_manager.graph_builder.graph_builder_ABC import GraphBuilder
from slam.frontend_manager.graph_builder.graph_builder_factory import (
    GraphBuilderFactory,
)

logger = logging.getLogger(__name__)


class FrontendManager:
    """
    Manages all frontend procedures: process measurements, build graph, detect loops and anomalies...
    """

    def __init__(self, config: DictConfig):
        self.graph: Graph = Graph()
        self.graph_builder: GraphBuilder = GraphBuilderFactory.create(config.graph_builder)

    def create_graph(self, batch: DataBatch) -> None:
        """
        Creates main graph by merging sub-graphs (graph candidates).

        create_graph_candidate(batch):
            1) Create graph candidate.
            2) Synchronize states of the candidate (squeeze them).
        merge(candidate, graph):
            3) For each state of the candidate:
                3.1) determine graph vertices.
                3.2) merge state with the main graph.
        4) Check if storage is empty after merge.

        Args:
            batch (DataBatch): data batch with elements.
        """
        self.graph_builder.create_graph_candidate(batch)
        candidate = self.graph_builder.graph_candidate
        self.graph_builder.merge(candidate, self.graph)
