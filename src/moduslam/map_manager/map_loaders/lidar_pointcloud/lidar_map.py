import logging
from pathlib import Path

import open3d as o3d

from src.logger.logging_config import map_manager
from src.moduslam.map_manager.map_loaders.lidar_pointcloud.config import (
    LidarMapLoaderConfig,
)
from src.moduslam.map_manager.maps.pointcloud import PointCloudMap
from src.moduslam.map_manager.protocols import MapLoader
from src.utils.exceptions import ExternalModuleException

logger = logging.getLogger(map_manager)


class LidarMapLoader(MapLoader):
    """Lidar pointcloud map loader."""

    def __init__(self, config: LidarMapLoaderConfig) -> None:
        """
        Args:
            config: configuration for the loader.
        """
        self._dir_path = Path(config.directory)
        self._file_extension: str = config.file_extension
        self._file_name: str = config.name
        self._compress: bool = config.compress
        self._write_ascii: bool = config.write_ascii
        self._progress_bar: bool = config.progress_bar
        self._remove_nan: bool = config.remove_nan
        self._remove_infinity: bool = config.remove_infinity

    def save(self, lidar_map: PointCloudMap) -> None:
        """Saves lidar pointcloud map to the file.

        Args:
            lidar_map: lidar pointcloud map to save.

        Raises:
            ExternalModuleException: if failed to save the map using Open3D lib.
        """
        if not self._dir_path.exists():
            self._dir_path.mkdir(parents=True, exist_ok=True)

        file_path = self._dir_path / f"{self._file_name}.{self._file_extension}"
        try:
            o3d.io.write_point_cloud(
                filename=file_path.as_posix(),
                pointcloud=lidar_map.pointcloud,
                format=self._file_extension,
                write_ascii=self._write_ascii,
                compressed=self._compress,
                print_progress=self._progress_bar,
            )
        except Exception as e:
            msg = f"Failed to save the map to {file_path}. Error: {e}"
            logger.critical(msg)
            raise ExternalModuleException(msg)

    def load(self) -> PointCloudMap:
        """Loads the map.

        Returns:
            lidar pointcloud map instance.

        Raises:
            ExternalModuleException: if failed to load the map using Open3D lib.
        """
        file_path = self._dir_path / f"{self._file_name}.{self._file_extension}"
        try:
            pointcloud = o3d.io.read_point_cloud(
                filename=file_path.as_posix(),
                format=self._file_extension,
                print_progress=self._progress_bar,
                remove_nan_points=self._remove_nan,
                remove_infinite_points=self._remove_infinity,
            )
            logger.info(f"Map has been successfully loaded from {file_path}")

        except Exception as e:
            msg = f"Failed to load the map from {file_path}. Error: {e}"
            logger.critical(msg)
            raise ExternalModuleException(msg)
        else:
            lidar_map = PointCloudMap()
            lidar_map.pointcloud = pointcloud
            return lidar_map
