import logging

import gtsam

from slam.backend_manager.graph_solver import GraphSolver
from slam.frontend_manager.graph.graph import Graph
from slam.logger.logging_config import backend_manager

logger = logging.getLogger(backend_manager)


class BackendManager:
    """Manages the backend."""

    def __init__(self):
        self._graph_solver = GraphSolver()
        self._result_values = gtsam.Values()
        logger.debug("Backend Manager has been configured.")

    def solve(self, graph: Graph) -> None:
        """Solves the optimization problem and updates the graph.

        Args:
            graph: contains factor graph to be solved.
        """
        self._result_values = self._graph_solver.solve(graph)
        graph.update(self._result_values)
        logger.debug("Graph has been solved.")
