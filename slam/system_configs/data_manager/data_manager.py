from dataclasses import dataclass

from slam.system_configs.data_manager.batch_factory.batch_factory import (
    BatchFactoryConfig,
)


@dataclass
class DataManagerConfig:
    """Data manager configuration."""

    batch_factory: BatchFactoryConfig
