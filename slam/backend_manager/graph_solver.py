import gtsam

from slam.frontend_manager.graph.graph import Graph


class GraphSolver:
    """Graph Solver."""

    def __init__(self) -> None:
        self._params = gtsam.LevenbergMarquardtParams()

    def solve(self, graph: Graph) -> gtsam.Values:
        """Solves the optimization problem for the given non-linear factor graph and
        initial values.

        Args:
            graph (Graph): a graph with the factors to be solved.

        Returns:
            (gtsam.Values): calculated values.
        """
        optimizer = gtsam.LevenbergMarquardtOptimizer(
            graph.factor_graph, graph.gtsam_values, self._params
        )
        optimizer.optimizeSafely()
        result = optimizer.values()
        return result
