import logging

from moduslam.data_manager.manager import DataManager
from moduslam.logger.logging_config import main_manager
from phd.moduslam.backend_manager.manager import BackendManager
from phd.moduslam.frontend_manager.manager import FrontendManager
from phd.moduslam.main_manager.config import MainManagerConfig
from phd.moduslam.setup_manager.manager import SetupManager

logger = logging.getLogger(main_manager)


class MainManager:
    """Main Manager of the system."""

    def __init__(self, config: MainManagerConfig) -> None:
        """
        Args:
            config: configuration for all managers.
        """
        self._setup_manager = SetupManager(config.setup_manager)
        self._data_manager = DataManager(config.data_manager)
        self._frontend_manager = FrontendManager(config.frontend_manager)
        self._backend_manager = BackendManager()
        logger.info("The system has been successfully initialized.")

    def build_map(self) -> None:
        """Builds the map using data from the data manager."""

        logger.info("Creating new data batch...")
        self._data_manager.make_batch_sequentially()

        self._set_prior()

        self._process()

        logger.info("All processes have finished successfully.")

    def _process(self) -> None:
        """Creates graph and solves it."""
        logger.info("Processing the data batch...")

        data_batch = self._data_manager.batch_factory.batch
        graph = self._frontend_manager.graph

        while not data_batch.empty:
            self._frontend_manager.create_graph(data_batch)
            self._backend_manager.solve(graph)

        logger.info("The data batch has been successfully processed.")

    def _set_prior(self) -> None:
        """Sets prior for the graph."""
        self._frontend_manager.set_prior()
        self._backend_manager.solve(self._frontend_manager.graph)
