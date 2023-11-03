from dataclasses import dataclass, field

from configs.system.data_manager.datasets.base_dataset import DatasetConfig
from configs.system.data_manager.memory import MemoryAnalyzerConfig
from configs.system.data_manager.regime import RegimeConfig


@dataclass
class DataManagerConfig:
    """
    Configures DataManager.
    """
    regime: RegimeConfig = field(default_factory=RegimeConfig)
    dataset: DatasetConfig = field(default_factory=DatasetConfig)
    memory: MemoryAnalyzerConfig = field(default_factory=MemoryAnalyzerConfig)
