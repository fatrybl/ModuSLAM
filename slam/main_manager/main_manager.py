import logging

from slam.backend_manager.backend_manager import BackendManager
from slam.data_manager.data_manager import DataManager
from slam.frontend_manager.frontend_manager import FrontendManager
from slam.map_manager.map_manager import MapManager
from slam.setup_manager.setup_manager import SetupManager
from slam.system_configs.system.main_manager import MainManagerConfig
from slam.utils.stopping_criterion import StoppingCriterion

logger = logging.getLogger(__name__)


class MainManager:
    """Main Manager of the system.

    Initializes other managers.
    """

    def __init__(self, cfg: MainManagerConfig) -> None:
        """Main Manager of the system.

        Args:
            cfg (MainManagerConfig): main config for all managers.
        """
        self.setup_manager = SetupManager(cfg.setup_manager)
        self.data_manager = DataManager(cfg.data_manager)
        self.frontend_manager = FrontendManager(cfg.frontend_manager)
        self.backend_manager = BackendManager()
        self.map_manager = MapManager()
        logger.info("The system has been successfully configured.")

    def process(
        self,
    ) -> None:
        """TODO Check if Memory breakpoint is valid before creating new batch."""
        batch = self.data_manager.batch_factory.batch
        graph = self.frontend_manager.graph
        while not batch.empty():
            self.frontend_manager.create_graph(batch)
            self.backend_manager.solve(graph)
            self.backend_manager.update(graph)

    def build_map(self) -> None:
        """
        TODO: check if break_point is still valid: batch might be deleted but Memory Criterion is still active.
        """
        while not StoppingCriterion.is_active():
            self.data_manager.make_batch()
            self.process()

        self.map_manager.create_map(self.frontend_manager.graph, self.data_manager.batch_factory)
        # self.map_manager.visualize_map()
        # self.map_manager.save_map()

        logger.info("Map has been built")
