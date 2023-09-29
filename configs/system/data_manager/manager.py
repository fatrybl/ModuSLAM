from dataclasses import dataclass, field

from configs.system.data_manager.datasets.base_dataset import Dataset
from configs.system.data_manager.memory import MemoryAnalyzer


@dataclass
class DataManager:
    dataset: Dataset
    memory: MemoryAnalyzer = field(default_factory=MemoryAnalyzer)
