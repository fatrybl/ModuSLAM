import logging

import psutil

from slam.system_configs.system.data_manager.batch_factory.memory import (
    MemoryAnalyzerConfig,
)

logger = logging.getLogger(__name__)


class MemoryAnalyzer:
    """Analyzes current memory usage."""

    def __init__(self, cfg: MemoryAnalyzerConfig) -> None:
        """

        Args:
            cfg (MemoryAnalyzerConfig): config with parameters.
        """
        assert cfg.batch_memory > 0, "Batch memory is 0"
        self._batch_memory_percent: float = cfg.batch_memory

    @property
    def total_memory(self) -> int:
        """Computes total physical memory available in bytes.

        Returns:
            int: total physical memory available in bytes.
        """
        return psutil.virtual_memory().total

    @property
    def available_memory_percent(self) -> float:
        """Computes the percentage of available memory.

        Returns:
            float: _description_
        """
        assert self.total_memory > 0, "Total memory is 0"

        available_percent: float = (psutil.virtual_memory().available / self.total_memory) * 100
        return available_percent

    @property
    def used_memory_percent(self) -> float:
        """Computes the percentage of used memory.

        Returns:
            float: the percentage of used memory
        """
        return psutil.virtual_memory().percent

    @property
    def permissible_memory_percent(self) -> float:
        """Computes the permissible percentage of memory which is available for the
        user.

        Returns:
            float: the permissible percentage of memory which is available for the user
        """
        return self._batch_memory_percent
