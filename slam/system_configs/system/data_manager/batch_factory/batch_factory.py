from dataclasses import dataclass

from slam.system_configs.system.data_manager.batch_factory.datasets.base_dataset import (
    DatasetConfig,
)
from slam.system_configs.system.data_manager.batch_factory.memory import (
    MemoryAnalyzerConfig,
)
from slam.system_configs.system.data_manager.batch_factory.regime import RegimeConfig


@dataclass
class BatchFactoryConfig:
    """Configures DataManager."""

    memory: MemoryAnalyzerConfig
    dataset: DatasetConfig
    regime: RegimeConfig
