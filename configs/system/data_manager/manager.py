from abc import ABC
from dataclasses import dataclass

from omegaconf import MISSING

from configs.system.data_manager.datasets.base_dataset import Dataset
from configs.system.data_manager.memory import MemoryAnalyzer


@dataclass
class Regime(ABC):
    """abstract regime of data flow"""
    name: str = MISSING


@dataclass
class TimeRange(Regime):
    """Data flow is limited by time range"""
    start: int = MISSING
    stop: int = MISSING
    name: str = "TimeRange"


@dataclass
class Stream(Regime):
    """Free data flow: all data without time limitations"""
    name: str = "Stream"


@dataclass
class DataManager:
    regime: Regime = MISSING
    dataset: Dataset = MISSING
    memory: MemoryAnalyzer = MISSING
