import logging
from typing import Type

from slam.frontend_manager.graph.edges import Edge
from slam.frontend_manager.graph.graph import Graph
from slam.frontend_manager.graph.graph_candidate import State

logger = logging.getLogger(__name__)


class GraphMerger:

    def __init__(self, ) -> None:
        self.edges = []
        self._handler_edge_table = None

    def __from_measurements(self, instance, measurements) -> tuple:
        edges = tuple()
        for m in measurements:
            edge = instance.create(m)
            edges += edge
        return edges

    def _construct(self, edge_instances, measurements) -> tuple:
        edges = tuple()
        for instance in edge_instances:
            new_edges = __from_measurements(instance, measurements)
            edges += new_edges
        return edges

    def _create_edges(self, state: State) -> tuple[Type[Edge]]:
        edges: tuple[Type[Edge]] = tuple()
        for handler, measurements in state.storage.data:
            edge_instances = self._handler_edge_table[handler]
            new_edges = self._construct(edge_instances, measurements)
            edges += new_edges
        return edges

    def connect(self, graph: Graph, states: list[State]):
        """
        Iterates through candidates -> vertices per candidate -> measurements from external modules.
        TODO: remove dummy iteration through all unnecessary handlers.
        Args:
            graph (Graph): main graph to be connected with new vertices (candidates)
            states (list[states]): list of candidates to be connected with the graph.
                Each candidate might have multiple vertices.
            storage (MeasurementStorage): contains processed measurements for each external module.

        Returns:

        """
        for state in states:
            edges = self._create_edges(state)
            graph.add_edge(edges)
