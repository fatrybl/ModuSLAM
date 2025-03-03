"""Initializes the map manager components based on the configuration."""

import logging

from src.logger.logging_config import map_manager
from src.moduslam.map_manager.protocols import MapFactory, MapLoader, MapVisualizer

logger = logging.getLogger(map_manager)


class Initializer:

    @staticmethod
    def create_map_factory() -> MapFactory:
        """Creates a map factory based on the map type.

        Returns:
            map factory type.

        Raises:
            TypeError: if the map type is not supported.
        """
        raise NotImplementedError

    @staticmethod
    def create_map_loader() -> MapLoader:
        """Creates a map loader based on the map loader configuration.
        Returns:
            map loader type.

        Raises:
            TypeError: if the map loader type is not supported.
        """
        raise NotImplementedError

    @staticmethod
    def create_map_visualizer(map_type: str) -> MapVisualizer:
        """Creates a map visualizer based on the visualizer configuration.

        Args:
            map_type: type of the map.

        Returns:
            map visualizer type.

        Raises:
            TypeError: if the visualizer type is not supported.
        """
        raise NotImplementedError
