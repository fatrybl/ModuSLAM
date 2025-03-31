from typing import cast

from hydra.core.config_store import ConfigStore

from hydra import compose, initialize
from src.moduslam.data_manager.batch_factory.configs import BatchFactoryConfig
from src.moduslam.data_manager.batch_factory.data_readers.kaist.configs.base import (
    KaistConfig,
)
from src.moduslam.data_manager.batch_factory.data_readers.tum_vie.configs.base import (
    TumVieConfig,
)


def get_config() -> BatchFactoryConfig:
    cs = ConfigStore.instance()
    cs.store(name="base_factory", node=BatchFactoryConfig)
    cs.store(name="base_kaist_urban_dataset", node=KaistConfig)
    cs.store(name="base_tum_vie_dataset", node=TumVieConfig)

    with initialize(version_base=None, config_path="configs"):
        cfg = compose(config_name="config")
        config = cast(BatchFactoryConfig, cfg)

    return config
