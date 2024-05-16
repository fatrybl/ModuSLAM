import logging

from slam.backend_manager.backend_manager import BackendManager
from slam.data_manager.data_manager import DataManager
from slam.frontend_manager.frontend_manager import FrontendManager
from slam.logger.logging_config import main_manager
from slam.map_manager.map_manager import MapManager
from slam.setup_manager.setup_manager import SetupManager
from slam.system_configs.main_manager import MainManagerConfig
from slam.utils.stopping_criterion import StoppingCriterion

logger = logging.getLogger(main_manager)


class MainManager:
    """Main Manager of the system."""

    def __init__(self, config: MainManagerConfig) -> None:
        """
        Args:
            config: configuration for all managers.
        """
        self.setup_manager = SetupManager(config.setup_manager)
        self.data_manager = DataManager(config.data_manager)
        self.frontend_manager = FrontendManager(config.frontend_manager)
        self.map_manager = MapManager(config.map_manager)
        self.backend_manager = BackendManager()
        logger.info("The system has been successfully initialized.")

    def _process(
        self,
    ) -> None:
        """Creates graph and solves it."""
        logger.info("Processing the data batch...")

        data_batch = self.data_manager.batch_factory.batch
        graph = self.frontend_manager.graph

        self.frontend_manager.set_prior()

        while not data_batch.empty:
            self.frontend_manager.create_graph(data_batch)
            self.backend_manager.solve(graph)
            self.backend_manager.update(graph)

        logger.info("The data batch has been successfully processed.")

    def build_map(self) -> None:
        """Builds the map using the data from the data manager."""

        while not StoppingCriterion.is_active():
            logger.info("Creating new data batch...")
            self.data_manager.make_batch()
            self._process()

        print(self.frontend_manager.graph.gtsam_values)
        self.frontend_manager.graph.factor_graph.print()

        self.map_manager.save_graph(self.frontend_manager.graph)
        self.map_manager.create_map(self.frontend_manager.graph, self.data_manager.batch_factory)
        self.map_manager.visualize_map()

        logger.info("All processes have finished successfully.")
