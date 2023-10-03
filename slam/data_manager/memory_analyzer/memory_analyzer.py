import logging
import psutil

from slam import logger
from configs.system.data_manager.memory import MemoryAnalyzer as MemoryAnalyzerConfig

logger = logging.getLogger(__name__)


class MemoryAnalyzer():
    def __init__(self, cfg: MemoryAnalyzerConfig):
        self.__graph_memory_percent: float = cfg.graph_memory

    @property
    def total_memory(self) -> int:
        return psutil.virtual_memory().total

    @property
    def available_memory_percent(self) -> float:
        available_percent: float = (
            psutil.virtual_memory().available / self.total_memory) * 100
        return available_percent

    @property
    def used_memory_percent(self):
        return psutil.virtual_memory().percent

    @property
    def permissible_memory_percent(self) -> float:
        return 100 - self.__graph_memory_percent
