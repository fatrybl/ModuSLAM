from abc import ABC, abstractmethod
import logging

from pathlib2 import Path

from configs.paths.DEFAULT_FILE_PATHS import ConfigFilePaths
from utils.config import Config
from data_manager.factory.readers.element_factory import Element


class DataReader(ABC):
    logger = logging.getLogger(__name__)

    def __init__(self):
        cfg = Config(
            ConfigFilePaths.data_manager_config).attributes["data"]
        self._dataset_dir = cfg["dataset_directory"]

    @staticmethod
    def check_file(file_path: Path) -> None:
        if not Path.is_file(file_path):
            raise FileNotFoundError
        if file_path.stat().st_size == 0:
            raise OSError("Empty input file")

    @abstractmethod
    def get_element(self) -> Element:
        """
        Gets element from dataset.
        Should be implemented for each reader
        """

    @abstractmethod
    def get_element_with_measurement(self, measurement: tuple) -> Element:
        """
        Args:
            measurement: 
                {"sensor": "camera_rgb_left",
                "location": {"file": Path(),
                             "position": 0}  }
        Gets element from dataset with particular sensor measurement.
        Should be implemented for each reader
        """
