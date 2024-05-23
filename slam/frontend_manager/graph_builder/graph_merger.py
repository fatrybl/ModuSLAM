import logging
from typing import Generic

from slam.frontend_manager.edge_factories.edge_factory_ABC import EdgeFactory
from slam.frontend_manager.graph.base_edges import GraphEdge
from slam.frontend_manager.graph.base_vertices import GraphVertex
from slam.frontend_manager.graph.graph import Graph
from slam.frontend_manager.graph_builder.candidate_factory.graph_candidate import State
from slam.frontend_manager.handlers.ABC_handler import Handler
from slam.logger.logging_config import frontend_manager
from slam.setup_manager.tables_initializer import init_handler_edge_factory_table

logger = logging.getLogger(frontend_manager)


class GraphMerger(Generic[GraphVertex, GraphEdge]):
    """Merges the graph candidate with the graph."""

    def __init__(self) -> None:
        self._table: dict[Handler, EdgeFactory] = {}

    @property
    def handler_edge_factory_table(self) -> dict[Handler, EdgeFactory]:
        """ "handler -> edge factory" table."""
        return self._table

    def init_table(self, config: dict[str, str]) -> None:
        """Initializes "handler -> edge factory" table.

        Args:
            config: "handler name -> edge factory name" pairs.

        Raises:
            ValueError: if the config is empty.
        """
        if config:
            self._table = init_handler_edge_factory_table(config)
        else:
            msg = "Empty config."
            logger.critical(msg)
            raise ValueError(msg)

    def merge(self, state: State, graph: Graph) -> None:
        """Merges the state with the graph.

        Args:
            state: a state to be merged with the graph.

            graph: a graph to merge the state with.
        """
        storage = state.data.items()
        state_time = state.timestamp

        for handler, measurements in storage:

            edge_factory = self._table[handler]
            edges = edge_factory.create(graph, measurements, state_time)
            graph.add_edges(edges)
