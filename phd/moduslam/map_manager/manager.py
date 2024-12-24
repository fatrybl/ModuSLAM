"""Manages all manipulations with the map."""

import logging
from typing import Any

from phd.logger.logging_config import map_manager
from phd.moduslam.data_manager.batch_factory.config_factory import (
    get_config as get_bf_config,
)
from phd.moduslam.data_manager.batch_factory.factory import BatchFactory
from phd.moduslam.frontend_manager.main_graph.graph import Graph
from phd.moduslam.map_manager.graph_saver import GraphSaver
from phd.moduslam.map_manager.map_factories.lidar_map.config_factory import (
    get_config as get_mf_config,
)
from phd.moduslam.map_manager.map_factories.lidar_map.factory import LidarMapFactory
from phd.moduslam.map_manager.visualizers.pointcloud import PointcloudVisualizer

logger = logging.getLogger(map_manager)


class MapManager:

    def __init__(self) -> None:
        map_factory_config = get_mf_config()
        bf_config = get_bf_config()
        self._graph_saver = GraphSaver()
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

    def save_map(self) -> None:
        """Saves the map."""
        raise NotImplementedError

    def save_graph(self, graph: Graph) -> None:
        """Saves the graph."""
        self._graph_saver.save_to_pdf(graph)
        logger.info("Graph has been saved.")
