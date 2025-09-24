import logging

import psutil

from moduslam.logger.logging_config import data_manager

logger = logging.getLogger(data_manager)


class MemoryAnalyzer:
    """Analyzes current memory usage."""

    def __init__(self, batch_memory_percent: float = 50.0) -> None:
        """
        Args:
            batch_memory_percent: permissible memory usage in percentage.
        """
        self._batch_memory_percent = batch_memory_percent

    @property
    def total_memory(self) -> int:
        """Computes total physical memory available in bytes."""
        return psutil.virtual_memory().total

    @property
    def available_memory_percent(self) -> float:
        """Percentage of available memory."""
        available_percent = (psutil.virtual_memory().available / self.total_memory) * 100
        return available_percent

    @property
    def used_memory_percent(self) -> float:
        """Percentage of used memory."""
        return psutil.virtual_memory().percent

    @property
    def permissible_memory_percent(self) -> float:
        """Permissible percentage of memory which is available for the user."""
        return self._batch_memory_percent

    @property
    def enough_memory(self) -> bool:
        """Checks if the memory usage is within the permissible limits."""
        if self.used_memory_percent < self.permissible_memory_percent:
            return True
        return False
