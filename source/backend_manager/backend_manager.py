import logging

class BackendManager():
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.solver = GraphSolver()

    def setup(self):
        cfg = Config()
        if cfg.compute_metrics:
            self.metrics = MetricsFactory()

    def solve(self):
        pass
