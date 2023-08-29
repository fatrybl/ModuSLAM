import logging

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from configs.paths.DEFAULT_FILE_PATHS import ConfigFilePaths
from slam.utils.config import Config
from slam.data_manager.factory.readers.element_factory import Element

logger = logging.getLogger(__name__)


class DataReader(ABC):
    def __init__(self):
        config = Config.from_file(
            ConfigFilePaths.data_manager_config.value)
        self._dataset_dir = config.attributes["data"]["dataset_directory"]

    @staticmethod
    def is_file_valid(file_path: Path) -> bool:
        if not Path.is_file(file_path):
            logger.critical(f"File {file_path} does not exist")
            return False
        if file_path.stat().st_size == 0:
            logger.critical(f"File {file_path} is empty")
            return False
        return True

    @abstractmethod
    def get_element(self, args: Any) -> Element:
        """
        Gets element from a dataset. 
        If no args: iterates through a dataset.
        if args: parces them in a dispatch method of a child class.
        Args:
            element: Data Batch element w/o raw sensor data
        Returns:
            element of type Element
        """
