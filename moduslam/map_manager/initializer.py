"""Initializes the map manager components based on the configuration."""

import logging
from typing import cast

from moduslam.frontend_manager.graph.custom_vertices import CameraPose
from moduslam.logger.logging_config import map_manager
from moduslam.map_manager.map_factories.lidar_map.factory import LidarMapFactory
from moduslam.map_manager.map_factories.trajectory.factory import TrajectoryMapFactory
from moduslam.map_manager.map_loaders.lidar_map import LidarMapLoader
from moduslam.map_manager.protocols import MapFactory, MapLoader, MapVisualizer
from moduslam.map_manager.visualizers.pointcloud import PointcloudVisualizer
from moduslam.map_manager.visualizers.trajectory import TrajectoryVisualizer
from moduslam.system_configs.map_manager.map_factories.lidar_map import (
    LidarMapFactoryConfig,
    MapFactoryConfig,
)
from moduslam.system_configs.map_manager.map_loaders.lidar_map import (
    LidarMapLoaderConfig,
)
from moduslam.system_configs.map_manager.map_manager import MapLoaderConfig
from moduslam.system_configs.map_manager.map_types import MapType

logger = logging.getLogger(map_manager)


class Initializer:

    @staticmethod
    def create_map_factory(config: MapFactoryConfig) -> MapFactory:
        """Creates a map factory based on the map type.

        Args:
            config: map factory configuration.

        Returns:
            map factory type.

        Raises:
            TypeError: if the map type is not supported.
        """
        match config.map_type:
            case MapType.trajectory:
                return TrajectoryMapFactory(pose_type=CameraPose)
            case MapType.lidar_pointcloud:
                lidar_cfg = cast(LidarMapFactoryConfig, config)
                return LidarMapFactory(lidar_cfg)
            case _:
                msg = f"Map type {config.map_type!r} is not supported. "
                logger.critical(msg)
                raise TypeError(msg)

    @staticmethod
    def create_map_loader(config: MapLoaderConfig) -> MapLoader:
        """Creates a map loader based on the map loader configuration.

        Args:
            config: map loader configuration.

        Returns:
            map loader type.

        Raises:
            TypeError: if the map loader type is not supported.
        """
        match config.map_type:
            case MapType.lidar_pointcloud:
                lidar_cfg = cast(LidarMapLoaderConfig, config)
                return LidarMapLoader(lidar_cfg)
            case _:
                msg = f"Map type {config.map_type!r} is not supported."
                logger.critical(msg)
                raise TypeError(msg)

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
        match map_type:
            case MapType.trajectory:
                return TrajectoryVisualizer()

            case MapType.lidar_pointcloud:
                return PointcloudVisualizer()
            case _:
                msg = f"Map type {map_type!r} is not supported."
                logger.critical(msg)
                raise TypeError(msg)
