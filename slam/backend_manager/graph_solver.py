import gtsam
from omegaconf import DictConfig

from slam.frontend_manager.graph.graph import Graph


class GraphSolver:
    """Factor Graph Solver."""

    def __init__(self, params: DictConfig) -> None:
        self.optimizer = gtsam.LevenbergMarquardtOptimizer
        self.params = gtsam.LevenbergMarquardtParams()
        self.init_values = gtsam.Values()

    def compute(self, graph: Graph):
        self.optimizer(graph.factor_graph, self.init_values, self.params)
        result = self.optimizer.optimizeSafely()
        return result
