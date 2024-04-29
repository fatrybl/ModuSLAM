import logging

import gtsam

from slam.backend_manager.graph_solver import GraphSolver
from slam.frontend_manager.graph.graph import Graph

logger = logging.getLogger(__name__)


class BackendManager:
    """Manages the backend."""

    def __init__(self):
        self._graph_solver = GraphSolver()
        self._result_values = gtsam.Values()

    def solve(self, graph: Graph) -> None:
        """Solves the optimization problem for the graph.

        Args:
            graph: contains factor graph to be solved.
        """
        self._result_values = self._graph_solver.solve(graph)

    def update(self, graph: Graph) -> None:
        """Updates the graph with the calculated values.

        Args:
            graph (Graph): a graph to be updated.
        """
        graph.update(self._result_values)
