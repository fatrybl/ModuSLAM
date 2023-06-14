import logging
from utils.config import Config
from configs.paths.DEFAULT_FILE_PATHS import ConfigFilePaths
from .solver import Solver
from .metrics_factory import MetricsFactory

class BackendManager():
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.solver = Solver()
        self.config = Config(ConfigFilePaths.backend_manager_config)
        if self.config.compute_metrics:
            self.metrics = MetricsFactory()

    def solve(self):
        pass
