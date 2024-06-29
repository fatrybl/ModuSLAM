import logging

from moduslam.data_manager.batch_factory.factory import BatchFactory
from moduslam.frontend_manager.graph.graph import Graph
from moduslam.logger.logging_config import map_manager
from moduslam.map_manager.graph_saver import GraphSaver
from moduslam.map_manager.map_factories.lidar_map.factory import LidarMapFactory
from moduslam.map_manager.map_factories.lidar_map.utils import PointcloudVisualizer
from moduslam.map_manager.map_loaders.lidar_map import MapLoader
from moduslam.map_manager.maps.pointcloud_map import PointcloudMap
from moduslam.system_configs.map_manager.map_manager import MapManagerConfig

logger = logging.getLogger(map_manager)


class MapManager:
    """Manages all manipulations with the map."""

    def __init__(self, config: MapManagerConfig) -> None:
        """
        Args:
            config: map manager configuration.
        """
        self._map_factory = LidarMapFactory(config.map_factory)
        self._map_loader = MapLoader(config.map_loader)
        self._graph_saver = GraphSaver()
        self._visualizer = PointcloudVisualizer()
        logger.debug("Map Manager has been configured.")

    @property
    def map(self) -> PointcloudMap:
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
