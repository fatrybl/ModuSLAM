import logging

from moduslam.data_manager.batch_factory.factory import BatchFactory
from moduslam.frontend_manager.graph.graph import Graph
from moduslam.logger.logging_config import map_manager
from moduslam.map_manager.graph_saver import GraphSaver
from moduslam.map_manager.map_factories.trajectory.factory import TrajectoryMapFactory
from moduslam.map_manager.visualizers.trajectory import TrajectoryVisualizer
from moduslam.system_configs.data_manager.batch_factory.batch_factory import (
    BatchFactoryConfig,
)
from moduslam.system_configs.map_manager.map_manager import MapManagerConfig

logger = logging.getLogger(map_manager)


class MapManager:
    """Manages all manipulations with the map."""

    def __init__(
        self, map_manager_config: MapManagerConfig, batch_factory_config: BatchFactoryConfig
    ) -> None:
        """
        Args:
            map_manager_config: map manager configuration.
        """
        self._batch_factory = BatchFactory(batch_factory_config)
        self._map_factory = TrajectoryMapFactory()
        # self._map_loader = MapLoader(map_manager_config.map_loader)
        self._graph_saver = GraphSaver()
        self._visualizer = TrajectoryVisualizer()
        logger.debug("Map Manager has been configured.")

    @property
    def map(self):
        """Map instance."""
        return self._map_factory.map

    def create_map(self, graph: Graph) -> None:
        """Creates a map from the graph.

        Args:
            graph (Graph): a graph to create a map from.
        """
        logger.info("Creating a map from the graph...")
        self._map_factory.create(graph.vertex_storage)

    def visualize_map(self) -> None:
        """Visualizes the map."""
        self._visualizer.visualize(self.map)

    # def save_map(self) -> None:
    #     """Saves the map."""
    #     self._map_loader.save(self.map)
    #     logger.info("Map has been saved.")

    def save_graph(self, graph: Graph) -> None:
        """Saves the graph.

        Args:
            graph: a graph to save.
        """
        self._graph_saver.save_to_pdf(graph)
        logger.info("Graph has been saved.")
