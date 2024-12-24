from typing import cast

from hydra import compose, initialize
from hydra.core.config_store import ConfigStore

from phd.moduslam.map_manager.map_factories.lidar_map.config import (
    LidarPointCloudConfig,
)


def get_config() -> LidarPointCloudConfig:
    cs = ConfigStore.instance()
    cs.store(name="base_lidar_pointcloud", node=LidarPointCloudConfig)

    with initialize(version_base=None, config_path="../configs"):
        cfg = compose(config_name="lidar_pointcloud")
        config = cast(LidarPointCloudConfig, cfg)

    return config
