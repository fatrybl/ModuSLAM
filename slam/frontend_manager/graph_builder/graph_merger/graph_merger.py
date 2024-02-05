import logging
from collections import deque

from slam.frontend_manager.elements_distributor.measurement_storage import Measurement
from slam.frontend_manager.graph.edges import Edge
from slam.frontend_manager.graph.edges_factories.handler_edge_table import (
    handler_edge_table,
)
from slam.frontend_manager.graph.graph import Graph
from slam.frontend_manager.graph.vertices import Vertex
from slam.frontend_manager.graph_builder.candidate_factory.graph_candidate import State
from slam.frontend_manager.handlers.ABC_handler import Handler

logger = logging.getLogger(__name__)


class GraphMerger:
    """
    Merges the graph candidate with the main graph.
    """

    def __init__(self) -> None:
        self._vertices: set[Vertex] = set()

    def _clear_storage(self, state: State) -> None:
        """
        Deletes measurements from the storage for the current state.
        Args:
            state (State): state with measurements.

        """
        ...

    def _determine_vertices(self, state: State) -> None:
        """
        Determines graph vertices for the state and fills in the set.
        1) Iterates over the state storage
        2) Takes predefined vertices for each handler
        3) Adds them to the set.

        Args:
            state (State): state with measurements.
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
            edge_factory = handler_edge_table[handler]
            new_edges = edge_factory.create(graph, self._vertices, measurements)
            edges += new_edges

        return edges

    def merge(self, state: State, graph: Graph) -> None:
        """
        Merges state with the graph.

        1) Determine graph vertices for the state.
        2) Create edges for the state using determined vertices.
        3) Remove state measurements from the storage.

        Args:
            state (State): new state to be merged with the graph.
            graph (Graph): main graph.

        """
        self._determine_vertices(state)
        edges = self._create_edges(state, graph)
        graph.add_edge(edges)
        self._clear_storage(state)
