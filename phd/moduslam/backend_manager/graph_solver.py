import logging

import gtsam

from phd.logger.logging_config import backend_manager
from phd.moduslam.frontend_manager.main_graph.graph import Graph

logger = logging.getLogger(backend_manager)


class GraphSolver:
    """Factor graph solver."""

    def __init__(self) -> None:
        self._params = gtsam.LevenbergMarquardtParams()
        self._params.setlambdaInitial(1e-1)

    def solve(self, graph: Graph) -> tuple[gtsam.Values, float]:
        """Solves the optimization problem for the given graph.

        Args:
            graph: contains factor graph to be solved.

        Returns:
            calculated GTSAM values and the corresponding error.
        """
        values = graph.get_backend_instances()
        optimizer = gtsam.LevenbergMarquardtOptimizer(graph.factor_graph, values, self._params)
        optimizer.optimize()
        result = optimizer.values()
        error = optimizer.error()
        logger.debug(f"optimization error: {error}")
        return result, error
