import logging

import psutil

from slam.logger.logging_config import data_manager
from slam.system_configs.data_manager.batch_factory.memory import MemoryAnalyzerConfig

logger = logging.getLogger(data_manager)


class MemoryAnalyzer:
    """Analyzes current memory usage."""

    def __init__(self, config: MemoryAnalyzerConfig) -> None:
        """
        Args:
            config: the configuration for the memory analyzer.
        """
        self._batch_memory_percent: float = config.batch_memory

    @property
    def total_memory(self) -> int:
        """Computes total physical memory available in bytes."""
        return psutil.virtual_memory().total

    @property
    def available_memory_percent(self) -> float:
        """Percentage of available memory."""
        available_percent: float = (psutil.virtual_memory().available / self.total_memory) * 100
        return available_percent

    @property
    def used_memory_percent(self) -> float:
        """Percentage of used memory."""
        return psutil.virtual_memory().percent

    @property
    def permissible_memory_percent(self) -> float:
        """Permissible percentage of memory which is available for the user."""
        return self._batch_memory_percent
