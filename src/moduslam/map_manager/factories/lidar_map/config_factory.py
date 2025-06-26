from typing import cast

from hydra.core.config_store import ConfigStore

from hydra import compose, initialize
from src.moduslam.map_manager.factories.lidar_map.config import (
    LidarPointCloudConfig,
)


def get_config() -> LidarPointCloudConfig:
    """Initializes and validates a Hydra-based configuration for processing point
    clouds.

    Returns:
        a configuration.
    """
    cs = ConfigStore.instance()
    cs.store(name="base_lidar_pointcloud", node=LidarPointCloudConfig)

    with initialize(version_base=None, config_path="../configs"):
        cfg = compose(config_name="config")
        config = cast(LidarPointCloudConfig, cfg)

    return config
