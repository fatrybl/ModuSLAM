import logging

from phd.logger.logging_config import main_manager
from phd.moduslam.backend_manager.manager import BackendManager
from phd.moduslam.data_manager.manager import DataManager
from phd.moduslam.frontend_manager.manager import FrontendManager
from phd.moduslam.setup_manager.manager import SetupManager

logger = logging.getLogger(main_manager)


class MainManager:
    """Main Manager of the system."""

    def __init__(self) -> None:
        self._setup_manager = SetupManager()
        self._data_manager = DataManager()
        self._frontend_manager = FrontendManager()
        self._backend_manager = BackendManager()
        logger.info("The system has been successfully initialized.")

    def build_map(self) -> None:
        """Builds the map using data from the data manager."""
        self._data_manager.make_batch_sequentially()

        data = self._data_manager.batch_factory.batch
        graph = self._frontend_manager.graph

        self._frontend_manager.set_prior()
        self._backend_manager.solve(graph)

        self._frontend_manager.create_graph(data)
        self._backend_manager.solve(graph)

        logger.info("The map has been built successfully.")
