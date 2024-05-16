import logging

from slam.data_manager.factory.batch_factory import BatchFactory
from slam.frontend_manager.graph.graph import Graph
from slam.logger.logging_config import map_manager
from slam.map_manager.graph_saver import GraphSaver
from slam.map_manager.map_factories.lidar_map_factory import LidarMapFactory
from slam.map_manager.map_factories.lidar_map_utils import (
    LidarMapLoader,
    PointcloudVisualizer,
)
from slam.map_manager.maps.lidar_map import LidarMap
from slam.system_configs.map_manager.map_manager import MapManagerConfig

logger = logging.getLogger(map_manager)


class MapManager:
    """Manages all manipulations with the map."""

    def __init__(self, config: MapManagerConfig) -> None:
        """
        Args:
            config: map manager configuration.
        """
        self._map_factory = LidarMapFactory(config.map_factory)
        self._map_loader = LidarMapLoader(config.map_loader)
        self._graph_saver = GraphSaver()
        self._visualizer = PointcloudVisualizer()
        logger.debug("Map Manager has been configured.")

    @property
    def map(self) -> LidarMap:
        """Map instance."""
        return self._map_factory.map

    def create_map(self, graph: Graph, batch_factory: BatchFactory) -> None:
        """Creates a map from the graph.

        Args:
            graph (Graph): a graph to create a map from.

            batch_factory: batch factory to create a data batch with map elements.
        """
        logger.info("Creating a map from the graph...")
        self._map_factory.create(graph.vertex_storage, graph.edge_storage, batch_factory)
        logger.info("Map has been created.")

    def visualize_map(self) -> None:
        """Visualizes the map."""
        self._visualizer.visualize(self.map.pointcloud)

    def save_map(self) -> None:
        """Saves the map."""
        self._map_loader.save(self.map)
        logger.info("Map has been saved.")

    def save_graph(self, graph: Graph) -> None:
        """Saves the graph.

        Args:
            graph: a graph to save.
        """
        self._graph_saver.save_to_pdf(graph)
        logger.info("Graph has been saved.")
