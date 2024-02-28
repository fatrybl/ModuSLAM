from dataclasses import dataclass

from slam.system_configs.system.data_manager.batch_factory.batch_factory import (
    BatchFactoryConfig,
)


@dataclass
class DataManagerConfig:
    batch_factory: BatchFactoryConfig
