import logging

import gtsam
from hydra.core.hydra_config import HydraConfig

from slam.frontend_manager.graph.graph import Graph

logger = logging.getLogger(__name__)


class GraphSolver:
    def __init__(self, params) -> None:
        self.optimizer = gtsam.LevenbergMarquardtOptimizer
        self.params = gtsam.LevenbergMarquardtParams()
        self.init_values = gtsam.Values()

    def compute(self, graph: Graph):
        self.optimizer(graph.factor_graph, self.init_values, self.params)
        result = self.optimizer.optimizeSafely()
        return result


class BackendManager:
    def __init__(self, config: HydraConfig):
        self.solver = GraphSolver(config.solver)

    def solve(self, graph: Graph):
        result = self.solver.compute(graph)
        return result
