import logging

from omegaconf import DictConfig

from slam.backend_manager.graph_solver import GraphSolver
from slam.frontend_manager.graph.graph import Graph

logger = logging.getLogger(__name__)


class BackendManager:
    """Manages all the backends."""

    def __init__(self, config: DictConfig):
        self.solver = GraphSolver(config.graph_solver)

    def solve(self, graph: Graph) -> None: ...
