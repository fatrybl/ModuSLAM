import logging

from slam.data_manager.factory.batch_factory import BatchFactory
from slam.frontend_manager.graph.graph import Graph
from slam.map_manager.graph_saver import GraphSaver
from slam.map_manager.map_factories.lidar_map_factory import LidarMapFactory
from slam.map_manager.map_factories.lidar_map_utils import (
    LidarMapLoader,
    PointcloudVisualizer,
)
from slam.map_manager.maps.lidar_map import LidarMap
from slam.system_configs.system.map_manager.map_manager import MapManagerConfig

logger = logging.getLogger(__name__)


class MapManager:
    """Manages all map manipulations."""

    def __init__(self, config: MapManagerConfig) -> None:
        self._map_factory = LidarMapFactory(config.map_factory)
        self._map_loader = LidarMapLoader(config.map_loader)
        self._graph_saver = GraphSaver()
        self._visualizer = PointcloudVisualizer()

    @property
    def map(self) -> LidarMap:
        """Map instance.

        Returns:
            Map instance (LidarMap).
        """
        return self._map_factory.map

    def create_map(self, graph: Graph, batch_factory: BatchFactory) -> None:
        """Creates a map from the graph.

        Args:
            graph (Graph): graph to create the map from.
            batch_factory (BatchFactory): batch factory to create the batch.
        """
        logger.info("Creating a map from the graph.")
        self._map_factory.create(graph.vertex_storage, batch_factory)

    def visualize_map(self) -> None:
        """Visualizes the map."""
        self._visualizer.visualize(self.map.pointcloud)

    def save_map(self) -> None:
        """Saves the map."""
        self._map_loader.save(self.map)

    def save_graph(self, graph: Graph) -> None:
        """Saves the graph.

        Args:
            graph (Graph): graph to save.
        """
        self._graph_saver.save_to_pdf(graph)
        self._graph_saver.save_to_file(graph)
