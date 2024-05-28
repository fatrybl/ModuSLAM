from dataclasses import dataclass

from moduslam.system_configs.data_manager.batch_factory.datasets.base_dataset import (
    DatasetConfig,
)
from moduslam.system_configs.data_manager.batch_factory.memory import (
    MemoryAnalyzerConfig,
)
from moduslam.system_configs.data_manager.batch_factory.regime import RegimeConfig


@dataclass
class BatchFactoryConfig:
    """Batch factory configuration."""

    memory: MemoryAnalyzerConfig
    dataset: DatasetConfig
    regime: RegimeConfig
