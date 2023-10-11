from dataclasses import dataclass
import logging

from abc import ABC, abstractmethod
from pathlib import Path

from slam.data_manager.factory.readers.element_factory import Element
from slam.utils.auxiliary_dataclasses import PeriodicData

logger = logging.getLogger(__name__)


class DataReader(ABC):
    @staticmethod
    def _is_file_valid(file_path: Path) -> bool:
        if not Path.is_file(file_path):
            logger.critical(f"File {file_path} does not exist")
            return False
        elif file_path.stat().st_size == 0:
            logger.critical(f"File {file_path} is empty")
            return False
        else:
            return True

    @abstractmethod
    def get_element(self, args: list[Element] | set[PeriodicData] | None = None) -> Element:
        """
        Gets element from a dataset. 
        If no args: iterates through a dataset.
        if args: parces them in a dispatched method of a child class.
        Args:
            element: Data Batch element w/o raw sensor data
        Returns:
            element with data of type Element
        """


@dataclass
class DataFlowState(ABC):
    """Keeps up-to-date state of a data flow for the reader. 
    Should be implemented for each reader."""
