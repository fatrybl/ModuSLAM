import logging

from moduslam.backend_manager.manager import BackendManager
from moduslam.data_manager.manager import DataManager
from moduslam.frontend_manager.manager import FrontendManager
from moduslam.logger.logging_config import main_manager
from moduslam.map_manager.manager import MapManager
from moduslam.setup_manager.manager import SetupManager
from moduslam.system_configs.main_manager import MainManagerConfig

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
        self.map_manager = MapManager(config.map_manager, config.data_manager.batch_factory)
        self.backend_manager = BackendManager()
        logger.info("The system has been successfully initialized.")

    def build_map(self) -> None:
        """Builds the map using the data from the data manager."""

        self._set_prior()

        logger.info("Creating new data batch...")
        self.data_manager.make_batch_sequentially()
        self._process()

        self.map_manager.save_graph(self.frontend_manager.graph)
        self.map_manager.create_map(self.frontend_manager.graph)
        self.map_manager.visualize_map()

        logger.info("All processes have finished successfully.")

    def _process(
        self,
    ) -> None:
        """Creates graph and solves it."""
        logger.info("Processing the data batch...")

        data_batch = self.data_manager.batch_factory.batch
        graph = self.frontend_manager.graph

        while not data_batch.empty:
            self.frontend_manager.create_graph(data_batch)
            self.backend_manager.solve(graph)

        # self.frontend_manager.graph.factor_graph.print()
        logger.info("The data batch has been successfully processed.")

    def _set_prior(self) -> None:
        """Sets prior for the graph."""
        self.frontend_manager.set_prior()
        self.backend_manager.solve(self.frontend_manager.graph)
