import logging

from omegaconf import DictConfig

from slam.backend_manager.graph_solver import GraphSolver
from slam.frontend_manager.graph.graph import Graph

logger = logging.getLogger(__name__)


class BackendManager:
    """Manages all the backends."""

    def __init__(self, config: DictConfig):
        self.graph_solver = GraphSolver(config.graph_solver)

    def solve(self, graph: Graph) -> None:
        """Solves the optimization problem for the given graph.

        Args:
            graph (Graph): a graph with the factors to be solved.
        """
        self.graph_solver.solve(graph)
