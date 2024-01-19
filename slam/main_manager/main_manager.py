import logging

from configs.main_config import Config
from slam.backend_manager.backend_manager import BackendManager
from slam.data_manager.data_manager import DataManager
from slam.data_manager.factory.batch import DataBatch
from slam.frontend_manager.frontend_manager import FrontendManager
from slam.frontend_manager.graph.graph import Graph
from slam.setup_manager.setup_manager import SetupManager
from slam.utils.meta_singleton import MetaSingleton
from slam.utils.stopping_criterion import StoppingCriterionSingleton

logger = logging.getLogger(__name__)


class MainManager(metaclass=MetaSingleton):
    def __init__(self, cfg: Config) -> None:
        """Initializes all managers

        Args:
            cfg (Config): main config for all managers.
        """
        self.break_point = StoppingCriterionSingleton()
        self.setup_manager = SetupManager(cfg.setup_manager)
        self.data_manager = DataManager(cfg.data_manager)
        self.frontend_manager = FrontendManager(cfg.frontend_manager)
        self.backend_manager = BackendManager(cfg.backend_manager)
        logger.info("The system has been successfully configured")

    def process(
        self,
    ) -> None:
        batch: DataBatch = self.data_manager.batch_factory.batch
        graph: Graph = self.frontend_manager.graph
        while not batch.empty():
            self.frontend_manager.create_graph(batch)
            self.backend_manager.solve(graph)

        # TODO Check if Memory breakpoint is valid before creating new batch.

    def build_map(self) -> None:
        """
        TODO: check if break_point is still valid:
        batch might be deleted but Memory Criterion is still active.
        """
        while not self.break_point.ON:
            self.data_manager.make_batch()
            self.process()

        logger.info("Map has been built")
