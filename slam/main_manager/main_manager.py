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
    """Main Manager of the system."""

    def __init__(self, config: MainManagerConfig) -> None:
        """
        Args:
            config (MainManagerConfig): main config for all managers.
        """
        self.setup_manager = SetupManager(config.setup_manager)
        self.data_manager = DataManager(config.data_manager)
        self.frontend_manager = FrontendManager(config.frontend_manager)
        self.map_manager = MapManager(config.map_manager)
        self.backend_manager = BackendManager()
        logger.info("The system has been successfully configured.")

    def _process(
        self,
    ) -> None:
        """TODO Check if Memory breakpoint is valid before creating new batch."""
        batch = self.data_manager.batch_factory.batch
        graph = self.frontend_manager.graph

        self.frontend_manager.set_prior()

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
            self._process()

        self.map_manager.create_map(self.frontend_manager.graph, self.data_manager.batch_factory)
        print(self.frontend_manager.graph.gtsam_values)
        self.map_manager.visualize_map()
        self.map_manager.save_graph(self.frontend_manager.graph)

        logger.info("Map has been built")
