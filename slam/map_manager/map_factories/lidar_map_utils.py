import logging
from pathlib import Path

import open3d as o3d

from slam.map_manager.maps.lidar_map import LidarMap
from slam.system_configs.system.map_manager.map_manager import LidarMapLoaderConfig
from slam.utils.exceptions import ExternalModuleException

logger = logging.getLogger(__name__)


class LidarMapLoader:
    """Class to load and save the lidar map."""

    def __init__(self, config: LidarMapLoaderConfig) -> None:
        self._dir_path: Path = Path(config.directory)
        self._file_extension: str = config.file_extension
        self._file_name: str = config.name
        self._compress: bool = config.compress
        self._write_ascii: bool = config.write_ascii
        self._progress_bar: bool = config.progress_bar
        self._remove_nan: bool = config.remove_nan
        self._remove_infinity: bool = config.remove_infinity

    def save(self, lidar_map: LidarMap) -> None:
        """Saves lidar map to the file.

        Args:
            lidar_map (LidarMap): map to save.
        """
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

    def load(self) -> LidarMap:
        """Loads the map.

        Returns:
            lidar map instance (LidarMap).
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
            lidar_map = LidarMap()
            lidar_map.pointcloud = pointcloud
            return lidar_map


class PointcloudVisualizer:
    """Class to visualize the pointcloud."""

    @staticmethod
    def visualize(pointcloud: o3d.geometry.PointCloud) -> None:
        """Visualizes the pointcloud.

        Args:
            pointcloud (np.ndarray[N,3]): pointcloud to visualize.
        """
        vis = o3d.visualization.Visualizer()
        vis.create_window()
        vis.add_geometry(pointcloud)
        vis.run()
