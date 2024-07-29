import logging

import gtsam

from moduslam.frontend_manager.graph.graph import Graph
from moduslam.logger.logging_config import backend_manager

logger = logging.getLogger(backend_manager)


class GraphSolver:
    """Factor graph solver."""

    def __init__(self) -> None:
        self._params = gtsam.LevenbergMarquardtParams()
        self._params.setlambdaInitial(1e-1)

    def solve(self, graph: Graph) -> gtsam.Values:
        """Solves the optimization problem for the given graph.

        Args:
            graph: contains factor graph to be solved.

        Returns:
            calculated GTSAM values.
        """

        optimizer = gtsam.LevenbergMarquardtOptimizer(
            graph.factor_graph, graph.backend_values, self._params
        )
        optimizer.optimize()
        result = optimizer.values()
        logger.debug(f"result: {result}")
        logger.debug(f"optimization error: {optimizer.error()}")
        return result
