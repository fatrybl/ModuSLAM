from dataclasses import dataclass, field

from configs.system.data_manager.batch_factory.batch_factory import BatchFactoryConfig


@dataclass
class DataManagerConfig:
    batch_factory: BatchFactoryConfig = field(
        default_factory=BatchFactoryConfig)
