import logging

from moduslam.frontend_manager.edge_factories.interface import EdgeFactory
from moduslam.frontend_manager.graph.graph import Graph
from moduslam.frontend_manager.graph_builder.candidate_factory.graph_candidate import (
    State,
)
from moduslam.frontend_manager.handlers.interface import Handler
from moduslam.logger.logging_config import frontend_manager
from moduslam.setup_manager.tables_initializer import init_handler_edge_factory_table

logger = logging.getLogger(frontend_manager)


class GraphMerger:
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

        for handler, measurements in storage:
            edge_factory = self._table[handler]
            edges = edge_factory.create(graph, measurements, state.timestamp)
            graph.add_edges(edges)
