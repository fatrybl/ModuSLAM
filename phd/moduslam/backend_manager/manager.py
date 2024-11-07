import logging

import gtsam

from moduslam.logger.logging_config import backend_manager
from phd.moduslam.backend_manager.graph_solver import GraphSolver
from phd.moduslam.frontend_manager.main_graph.graph import Graph

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
        graph.update_vertices(self._result_values)
