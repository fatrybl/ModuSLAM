import logging

from configs.main_config import MainConfig
from slam.data_manager.data_manager import DataManager
from slam.setup_manager.setup_manager import SetupManager
from slam.utils.stopping_criterion import StoppingCriterion

logger = logging.getLogger(__name__)


class MainManager:
    """
    Main Manager of the system. Initializes other managers.
    """

    def __init__(self, cfg: MainConfig) -> None:
        """Main Manager of the system.

        Args:
            cfg (Config): main config for all managers.
        """
        self.break_point = StoppingCriterion
        self.setup_manager = SetupManager(cfg.setup_manager)
        self.data_manager = DataManager(cfg.data_manager)
        # self.frontend_manager = FrontendManager(cfg.frontend_manager)
        # self.backend_manager = BackendManager(cfg.backend_manager)
        logger.info("The system has been successfully configured")

    # def process(
    #     self,
    # ) -> None:
    #     batch: DataBatch = self.data_manager.batch_factory.batch
    #     graph: Graph = self.frontend_manager.graph
    #     while not batch.empty():
    #         self.frontend_manager.create_graph(batch)
    #         self.backend_manager.solve(graph)
    #
    # TODO Check if Memory breakpoint is valid before creating new batch.

    def build_map(self) -> None:
        """
        TODO: check if break_point is still valid:
        batch might be deleted but Memory Criterion is still active.
        """
        while not self.break_point.is_active():
            self.data_manager.make_batch()

        # b = self.data_manager.batch_factory.batch
        logger.info("Map has been built")
