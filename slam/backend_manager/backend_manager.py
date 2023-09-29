import logging
from .solver import Solver
from .metrics_factory import MetricsFactory

class BackendManager():
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.solver = Solver()
        if self.config.compute_metrics:
            self.metrics = MetricsFactory()

    def solve(self):
        pass
