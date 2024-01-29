import logging

from slam.frontend_manager.elements_distributor.measurement_storage import (
    MeasurementStorage,
)
from slam.frontend_manager.graph.edges.base_edge import Edge
from slam.frontend_manager.graph.graph import Graph
from slam.frontend_manager.graph.graph_candidate import GraphCandidate, State

logger = logging.getLogger(__name__)


class GraphMerger:
    def __init__(
        self,
    ) -> None:
        self._handler_edgeFactory_table = None

    @staticmethod
    def _construct(graph: Graph, edges_factories, measurements) -> list[Edge]:
        edges: list[Edge] = []
        for factory in edges_factories:
            new_edges = factory.create(graph, measurements)
            edges += (new_edges,)
        return edges

    def _create_edges(self, graph: Graph, state: State) -> list[Edge]:
        edges: list[Edge] = []
        storage: MeasurementStorage = state.storage
        for handler, measurements in storage.data:
            edges_factories = self._handler_edgeFactory_table[handler]
            new_edges = self._construct(graph, edges_factories, measurements)
            edges += (new_edges,)
        return edges

    def connect(self, graph: Graph, candidate: GraphCandidate) -> None:
        """
        Connects the given graph with the given candidate.
        Args:
            candidate (GraphCandidate): graph candidate to be merged into Graph.
            graph (Graph): main graph to be connected with new vertices (candidates).
        """
        for state in candidate.states:
            edges = self._create_edges(graph, state)
            graph.add_edge(edges)
