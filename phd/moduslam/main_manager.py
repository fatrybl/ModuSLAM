import logging

from phd.logger.logging_config import main_manager
from phd.measurement_storage.storage import MeasurementStorage
from phd.moduslam.backend_manager.manager import BackendManager
from phd.moduslam.data_manager.manager import DataManager
from phd.moduslam.frontend_manager.manager import FrontendManager
from phd.moduslam.map_manager.manager import MapManager

logger = logging.getLogger(main_manager)


class MainManager:
    """Main Manager of the system."""

    def __init__(self) -> None:
        self._data_manager = DataManager()
        self._frontend_manager = FrontendManager()
        self._backend_manager = BackendManager()
        self._map_manager = MapManager()
        logger.info("The system has been successfully initialized.")

    def build_map(self) -> None:
        """Builds the map using data from the data manager."""
        priors = self._frontend_manager.create_prior_measurements()
        for measurement in priors:
            MeasurementStorage.add(measurement)

        self._data_manager.make_batch_sequentially()
        data = self._data_manager.batch_factory.batch

        self._frontend_manager.create_graph(data)

        graph = self._frontend_manager.graph

        self._backend_manager.solve(graph)

        self._map_manager.save_graph(graph)
        self._map_manager.create_map(graph)
        self._map_manager.visualize_map()

        logger.info("The map has been built successfully.")
