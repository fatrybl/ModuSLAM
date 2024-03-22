import gtsam
from omegaconf import DictConfig

from slam.frontend_manager.graph.graph import Graph


class GraphSolver:
    """Graph Solver.

    TODO: add optimize_using from GTSAM logging_optimizer.py for better debugging.
    """

    def __init__(self, params: DictConfig) -> None:
        self._optimizer = gtsam.LevenbergMarquardtOptimizer
        self._params = gtsam.LevenbergMarquardtParams()
        self._init_values = gtsam.Values()

    def compute(self, factor_graph: gtsam.NonlinearFactorGraph) -> gtsam.Values:
        """Solves the optimization problem for the given non-linear factor graph.

        Args:
            factor_graph (gtsam.NonlinearFactorGraph): factor graph to be optimized.

        Returns:
            (gtsam.Values): optimized values.
        """
        self._optimizer(factor_graph, self._init_values, self._params)
        self._optimizer.optimizeSafely()
        return self._optimizer.values()

    def solve(self, graph: Graph) -> None:
        """Solves the optimization problem for the given graph.

        Args:
            graph (Graph): a graph with the factors to be solved.
        """
        result = self.compute(graph.factor_graph)
        graph.update(result)
