from dataclasses import dataclass, field

from configs.system.data_manager.batch_factory.datasets.base_dataset import (
    DatasetConfig,
)
from configs.system.data_manager.batch_factory.memory import MemoryAnalyzerConfig
from configs.system.data_manager.batch_factory.regime import RegimeConfig


@dataclass
class BatchFactoryConfig:
    """
    Configures DataManager.
    """

    regime: RegimeConfig = field(default_factory=RegimeConfig)
    dataset: DatasetConfig = field(default_factory=DatasetConfig)
    memory: MemoryAnalyzerConfig = field(default_factory=MemoryAnalyzerConfig)
