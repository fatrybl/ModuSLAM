import gtsam

from phd.external.metrics.base import Metrics
from phd.moduslam.backend_manager.graph_solver import GraphSolver
from phd.moduslam.frontend_manager.main_graph.graph import Graph


class SolverError(Metrics):

    def __init__(self):
        self._solver = GraphSolver()

    def compute(self, graph: Graph) -> tuple[gtsam.Values, float]:
        """Computes solver error by solving the graph.

        Args:
            graph: a main graph.

        Returns:
            computed GTSAM values and solver error.
        """
        values, error = self._solver.solve(graph)

        return values, error
