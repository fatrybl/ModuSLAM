import logging

from system_configs.system.frontend_manager.frontend_manager import (
    FrontendManagerConfig,
)

from slam.data_manager.factory.batch import DataBatch
from slam.frontend_manager.graph.graph import Graph
from slam.frontend_manager.graph_builder.builders.graph_builder_ABC import GraphBuilder
from slam.frontend_manager.graph_builder.graph_builder_factory import (
    GraphBuilderFactory,
)

logger = logging.getLogger(__name__)


class FrontendManager:
    """
    Manages all frontend procedures: process measurements, build graph, detect loops and anomalies...
    """

    def __init__(self, config: FrontendManagerConfig):
        self.graph: Graph = Graph()
        self.graph_builder: GraphBuilder = GraphBuilderFactory.create(config.graph_builder)

    def create_graph(self, batch: DataBatch) -> None:
        """Creates main graph by merging sub-graphs (graph candidates).

        1) create_graph_candidate(batch).
        2) merge(candidate, graph).
        3) Check if storage is empty after merge.

        Args:
            batch (DataBatch): data batch with elements.
        """
        self.graph_builder.create_graph_candidate(batch)
        candidate = self.graph_builder.graph_candidate
        self.graph_builder.merge(candidate, self.graph)
