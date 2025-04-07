from typing import cast

from hydra.core.config_store import ConfigStore

from hydra import compose, initialize
from src.moduslam.data_manager.batch_factory.configs import BatchFactoryConfig
from src.moduslam.data_manager.batch_factory.data_readers.kaist.configs.base import (
    KaistConfig,
)
from src.moduslam.data_manager.batch_factory.data_readers.ros2.configs.base import (
    Ros2Humble,
)
from src.moduslam.data_manager.batch_factory.data_readers.tum_vie.configs.base import (
    TumVieConfig,
)


def get_config() -> BatchFactoryConfig:
    """Reads and validates the config file for Batch Factory."""

    cs = ConfigStore.instance()
    cs.store(name="base_factory", node=BatchFactoryConfig)
    cs.store(name="base_kaist_urban_dataset", node=KaistConfig)
    cs.store(name="base_tum_vie_dataset", node=TumVieConfig)
    cs.store(name="base_ros2_s3e_dataset", node=Ros2Humble)

    with initialize(version_base=None, config_path="configs"):
        cfg = compose(config_name="config")
        config = cast(BatchFactoryConfig, cfg)

    return config
