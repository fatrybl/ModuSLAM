import logging

import gtsam

from slam.backend_manager.graph_solver import GraphSolver
from slam.frontend_manager.graph.graph import Graph

logger = logging.getLogger(__name__)


class BackendManager:
    """Manages all the backends."""

    def __init__(self):
        self.graph_solver = GraphSolver()
        self.result_values = gtsam.Values()

    def solve(self, graph: Graph) -> None:
        """Solves the optimization problem for the given graph.

        Args:
            graph (Graph): a graph with the factors to be solved.
        """
        self.result_values = self.graph_solver.solve(graph)

    def update(self, graph: Graph) -> None:
        """Updates the graph with the optimized values.

        Args:
            graph (Graph): a graph to be updated.
        """
        graph.update(self.result_values)
