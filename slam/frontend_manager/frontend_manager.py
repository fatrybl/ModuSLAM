import logging

from slam.data_manager.factory.batch import DataBatch
from slam.frontend_manager.graph.graph import Graph
from slam.frontend_manager.graph_builder.graph_builder_ABC import GraphBuilder
from slam.frontend_manager.graph_builder.graph_builder_factory import (
    GraphBuilderFactory,
)
from slam.system_configs.system.frontend_manager.frontend_manager import (
    FrontendManagerConfig,
)

logger = logging.getLogger(__name__)


class FrontendManager:
    """
    Manages all frontend procedures: process measurements, build graph, detect loops and anomalies...
    """

    def __init__(self, config: FrontendManagerConfig):
        self.graph: Graph = Graph()
        builder_object: type[GraphBuilder] = GraphBuilderFactory.create(config.graph_builder.name)
        self.graph_builder: GraphBuilder = builder_object(config.graph_builder)

    def create_graph(self, batch: DataBatch) -> None:
        """Creates main graph by merging sub-graphs (graph candidates).

        Args:
            batch (DataBatch): data batch with elements.
        """
        self.graph_builder.create_graph_candidate(batch)
        self.graph_builder.merge_graph_candidate(self.graph)
        self.graph_builder.clear_candidate()
