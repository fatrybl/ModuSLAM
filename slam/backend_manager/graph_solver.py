import gtsam

from slam.frontend_manager.graph.graph import Graph


class GraphSolver:
    """Graph Solver.

    TODO: add optimize_using from GTSAM logging_optimizer.py for better debugging.
    """

    def __init__(self) -> None:
        self._params = gtsam.LevenbergMarquardtParams()

    def compute(
        self, factor_graph: gtsam.NonlinearFactorGraph, init_values: gtsam.Values
    ) -> gtsam.Values:
        """Solves the optimization problem for the given non-linear factor graph.

        Args:
            factor_graph (gtsam.NonlinearFactorGraph): factor graph to be optimized.

        Returns:
            (gtsam.Values): optimized values.
        """
        optimizer = gtsam.LevenbergMarquardtOptimizer(factor_graph, init_values, self._params)
        optimizer.optimizeSafely()
        return optimizer.values()

    def solve(self, graph: Graph) -> gtsam.Values:
        """Solves the optimization problem for the given graph.

        Args:
            graph (Graph): a graph with the factors to be solved.
        """
        initial_estimate = gtsam.Values()
        vertices = graph.vertex_storage.optimizable_vertices
        [initial_estimate.insert(v.gtsam_index, v.value) for v in vertices]

        result = self.compute(graph.factor_graph, initial_estimate)
        return result
