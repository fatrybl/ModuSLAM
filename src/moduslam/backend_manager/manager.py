import logging

from moduslam.backend_manager.graph_solver import GraphSolver
from moduslam.frontend_manager.main_graph.graph import Graph
from moduslam.logger.logging_config import backend_manager

logger = logging.getLogger(backend_manager)


class BackendManager:
    """Manages the backend."""

    def __init__(self):
        self._graph_solver = GraphSolver()
        logger.debug("Backend Manager has been configured.")

    def solve(self, graph: Graph) -> None:
        """Solves the optimization problem and updates the graph.

        Args:
            graph: contains factor graph to be solved.
        """
        result_values, error = self._graph_solver.solve(graph)
        graph.update_vertices(result_values)
        logger.debug(result_values)
