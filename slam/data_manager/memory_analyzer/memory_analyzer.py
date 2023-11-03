import logging
import psutil

from slam import logger
from configs.system.data_manager.batch_factory.memory import MemoryAnalyzerConfig as MemoryAnalyzerConfig

logger = logging.getLogger(__name__)


class MemoryAnalyzer():
    """Analyzes current memory usage."""

    def __init__(self, cfg: MemoryAnalyzerConfig) -> None:
        """
        Attributes:
            __graph_memory_percent (float): the percentage of memory to store graph.
        Args:
            cfg (MemoryAnalyzerConfig): a config containing parameters.
        """

        if cfg.graph_memory not in range(0, 100):
            msg = f"Incorrect percentage of memory for the graph: out of range"
            logger.critical(msg)
            raise ValueError(msg)
        else:
            self.__graph_memory_percent: float = cfg.graph_memory

    @property
    def total_memory(self) -> int:
        """Computes total phisycal memory available in bytes.

        Returns:
            int: total phisycal memory available in bytes.
        """
        return psutil.virtual_memory().total

    @property
    def available_memory_percent(self) -> float:
        """Computes the percentage of available memory.

        Returns:
            float: _description_
        """
        available_percent: float = (
            psutil.virtual_memory().available / self.total_memory) * 100
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
        """Computes the permissible percentage of memory which is available for the user.

        Returns:
            float: the permissible percentage of memory which is available for the user
        """
        return 100 - self.__graph_memory_percent
