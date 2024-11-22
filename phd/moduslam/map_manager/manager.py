"""Manages all manipulations with the map."""

import logging
from typing import Any

from moduslam.data_manager.batch_factory.factory import BatchFactory
from moduslam.frontend_manager.graph.graph import Graph
from moduslam.logger.logging_config import map_manager
from moduslam.map_manager.graph_saver import GraphSaver
from moduslam.map_manager.initializer import Initializer
from moduslam.map_manager.map_factories.lidar_map.factory import LidarMapFactory
from moduslam.map_manager.map_factories.trajectory.factory import TrajectoryMapFactory
from moduslam.system_configs.data_manager.batch_factory.batch_factory import (
    BatchFactoryConfig,
)
from moduslam.system_configs.map_manager.map_manager import MapManagerConfig

logger = logging.getLogger(map_manager)


class MapManager:

    def __init__(
        self, manager_config: MapManagerConfig, batch_factory_config: BatchFactoryConfig
    ) -> None:
        """
        Args:
            manager_config: map manager configuration.

            batch_factory_config: batch factory configuration.
        """
        self._batch_factory = BatchFactory(batch_factory_config)
        self._map_factory = Initializer.create_map_factory(manager_config.map_factory)
        self._map_loader = Initializer.create_map_loader(manager_config.map_loader)
        self._map_visualizer = Initializer.create_map_visualizer(
            manager_config.map_factory.map_type
        )
        self._graph_saver = GraphSaver()
        logger.debug("Map Manager has been configured.")

    @property
    def map(self) -> Any:
        """Map instance."""
        return self._map_factory.map

    def create_map(self, graph: Graph) -> None:
        """Creates a map from the graph.

        Args:
            graph (Graph): a graph to create a map from.
        """
        logger.info("Creating a map from the graph...")

        factory_args_table = {
            TrajectoryMapFactory: (graph.vertex_storage,),
            LidarMapFactory: (graph, self._batch_factory),
        }

        args = factory_args_table[type(self._map_factory)]
        self._map_factory.create_map(*args)

        logger.info("Map has been created.")

    def visualize_map(self) -> None:
        """Visualizes the map."""
        self._map_visualizer.visualize(self._map_factory.map)

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
