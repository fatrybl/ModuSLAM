import gtsam

from slam.frontend_manager.graph.graph import Graph


class GraphSolver:
    """Factor graph solver."""

    def __init__(self) -> None:
        self._params = gtsam.LevenbergMarquardtParams()

    def solve(self, graph: Graph) -> gtsam.Values:
        """Solves the optimization problem for the given graph.

        Args:
            graph: contains factor graph to be solved.

        Returns:
            calculated GTSAM values.
        """
        optimizer = gtsam.LevenbergMarquardtOptimizer(
            graph.factor_graph, graph.gtsam_values, self._params
        )
        optimizer.optimizeSafely()
        result = optimizer.values()
        return result
