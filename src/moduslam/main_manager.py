import logging
from pathlib import Path

from src.logger.logging_config import main_manager
from src.measurement_storage.storage import MeasurementStorage
from src.moduslam.backend_manager.manager import BackendManager
from src.moduslam.data_manager.manager import DataManager
from src.moduslam.frontend_manager.manager import FrontendManager
from src.moduslam.map_manager.manager import MapManager

logger = logging.getLogger(main_manager)


class MainManager:
    """Main Manager of the system."""

    def __init__(self) -> None:
        self._data_manager = DataManager()
        self._frontend_manager = FrontendManager()
        self._backend_manager = BackendManager()
        self._map_manager = MapManager()
        self._trajectory_file = Path(__file__).parent / "trajectory.txt"
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

        self._map_manager.save_trajectory(graph, self._trajectory_file)
        self._map_manager.save_graph(graph)
        self._map_manager.create_map(graph)
        self._map_manager.save_map()

        self._map_manager.visualize_map()
        # self._map_manager.visualize_clusters(graph)

        logger.info(
            f"num clusters: {len(graph.vertex_storage.clusters)},"
            f"num edges: {len(graph.edges)},"
            f"num vertices: {len(graph.vertex_storage.vertices)}"
        )

        logger.info("The map has been built successfully.")
