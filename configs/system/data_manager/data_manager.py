from dataclasses import dataclass, field

from configs.system.data_manager.datasets.base_dataset import DatasetConfig
from configs.system.data_manager.memory import MemoryAnalyzer
from configs.system.data_manager.regime import Regime


@dataclass
class DataManager:
    """
    Configures DataManager.
    """
    regime: Regime = field(default_factory=Regime)
    dataset: DatasetConfig = field(default_factory=DatasetConfig)
    memory: MemoryAnalyzer = field(default_factory=MemoryAnalyzer)
