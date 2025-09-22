"""Manages all manipulations with the map."""

import logging
from pathlib import Path
from typing import Any

from moduslam.data_manager.batch_factory.config_factory import (
    get_config as get_bf_config,
)
from moduslam.data_manager.batch_factory.factory import BatchFactory
from moduslam.frontend_manager.main_graph.graph import Graph
from moduslam.logger.logging_config import map_manager
from moduslam.map_manager.factories.lidar_map.config_factory import (
    get_config as get_mf_config,
)
from moduslam.map_manager.factories.lidar_map.factory import LidarMapFactory
from moduslam.map_manager.graph_saver import GraphSaver
from moduslam.map_manager.loaders.lidar_pointcloud.config import (
    LidarMapLoaderConfig,
)
from moduslam.map_manager.loaders.lidar_pointcloud.lidar_map import (
    LidarMapLoader,
)
from moduslam.map_manager.trajectory import get_trajectory, save_trajectory_to_txt
from moduslam.map_manager.visualizers.graph_visualizer.data_factory import (
    create_data,
)
from moduslam.map_manager.visualizers.graph_visualizer.visualizer import draw
from moduslam.map_manager.visualizers.graph_visualizer.visualizer_params import (
    VisualizationParams,
)
from moduslam.map_manager.visualizers.pointcloud import PointcloudVisualizer

logger = logging.getLogger(map_manager)


class MapManager:

    def __init__(self) -> None:
        map_factory_config = get_mf_config()
        bf_config = get_bf_config()
        map_loader_config = LidarMapLoaderConfig()
        self._graph_saver = GraphSaver()
        self._map_loader = LidarMapLoader(map_loader_config)
        self._batch_factory = BatchFactory(bf_config)
        self._map_factory = LidarMapFactory(map_factory_config)
        self._map_visualizer = PointcloudVisualizer
        logger.debug("Map Manager has been configured.")

    @property
    def map(self) -> Any:
        """Map instance."""
        return self._map_factory.map

    def create_map(self, graph: Graph) -> None:
        """Creates a map from the graph.

        Args:
            graph: the main graph to create a map from.
        """
        logger.info("Creating a map from the graph...")

        self._map_factory.create_map(graph, self._batch_factory)

        logger.info("Map has been created.")

    def visualize_map(self) -> None:
        """Visualizes the map."""
        self._map_visualizer.visualize(self._map_factory.map)

    @staticmethod
    def visualize_clusters(graph: Graph) -> None:
        """Visualizes clusters of the graph.

        Args:
            graph: a graph with clusters to visualize.
        """
        vis_data = create_data(graph)
        params = VisualizationParams()
        draw(vis_data, params)

    def save_map(self) -> None:
        """Saves the map."""
        self._map_loader.save(self.map)

    def save_graph(self, graph: Graph) -> None:
        """Saves the graph."""
        self._graph_saver.save_to_pdf(graph)
        # self._graph_saver.save_to_file(graph)
        logger.info("Graph has been saved.")

    @staticmethod
    def save_trajectory(graph: Graph, path: Path) -> None:
        """Saves the trajectory to the file.

        Args:
            graph: a graph to get the trajectory from.

            path: a path to the file to save the trajectory.
        """
        clusters = graph.vertex_storage.sorted_clusters
        trajectory = get_trajectory(clusters)
        save_trajectory_to_txt(path, trajectory)
