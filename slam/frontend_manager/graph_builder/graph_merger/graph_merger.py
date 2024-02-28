import logging
from collections import deque

from configs.system.frontend_manager.graph_builder.graph_merger.merger import (
    GraphMergerConfig,
)
from slam.frontend_manager.element_distributor.measurement_storage import Measurement
from slam.frontend_manager.graph.edges import Edge
from slam.frontend_manager.graph.edges_factories.edge_factory_ABC import EdgeFactory
from slam.frontend_manager.graph.graph import Graph
from slam.frontend_manager.graph.vertices import Vertex
from slam.frontend_manager.graph_builder.candidate_factory.graph_candidate import State
from slam.frontend_manager.handlers.ABC_handler import Handler
from slam.setup_manager.edge_factories_initializer.factory import EdgeCreatorFactory
from slam.setup_manager.handlers_factory.factory import HandlerFactory

logger = logging.getLogger(__name__)


class GraphMerger:
    """Merges the graph candidate with the main graph."""

    def __init__(self, config: GraphMergerConfig) -> None:
        self._vertices: set[Vertex] = set()
        self._table: dict[Handler, EdgeFactory] = {}
        self._fill_table(config.handler_edge_factory_table)

    def _fill_table(self, config: dict[str, str]) -> None:
        """Fills in the table which represents handler -> edge factory connections.

        Args:
            config (dict[str, str]): configuration.
        """
        for handler_name, edge_factory_name in config.items():
            handler: Handler = HandlerFactory.get_handler(handler_name)
            edge_factory: EdgeFactory = EdgeCreatorFactory.get_factory(edge_factory_name)
            self._table[handler] = edge_factory

    def _clear_storage(self, state: State) -> None:
        """Deletes measurements from the storage for the current state.

        Args:
            state (State): state with measurements.
        """
        ...

    def _init_vertices(self, state: State) -> None:
        """Determines graph vertices for the state and fills in the set. 1) Iterates
        over the state storage 2) Takes predefined vertices for each handler 3) Adds
        them to the set.

        Args:
            state (State): state with measurements.

        TODO: Add the implementation.
        """
        ...

    def _create_edges(self, state: State, graph: Graph) -> list[Edge]:
        """
        Creates edges for the state.
        Note:
            Each handler is being processed by the corresponding edge factory.

        Args:
            state (State): state with measurements.
            graph (Graph): main graph.

        Returns:
            (list[Edge]): new edges.
        """
        edges: list[Edge] = []
        data: dict[Handler, deque[Measurement]] = state.storage.data

        for handler, measurements in data.items():
            edge_factory = self._table[handler]
            new_edges = edge_factory.create(graph, self._vertices, measurements)
            edges += new_edges

        return edges

    @property
    def handler_edge_factory_table(self) -> dict[Handler, EdgeFactory]:
        """A table to represent the connections between handlers & edge factories.

        Returns:
            (dict[Handler, EdgeFactory]): handler -> edge factory table.
        """
        return self._table

    def merge(self, state: State, graph: Graph) -> None:
        """Merges state with the graph.

        1) Determine graph vertices for the state.
        2) Create edges for the state using determined vertices.
        3) Remove state measurements from the storage.

        Args:
            state (State): new state to be merged with the graph.
            graph (Graph): main graph.
        """
        self._init_vertices(state)
        edges = self._create_edges(state, graph)
        graph.add_edge(edges)
        self._clear_storage(state)
