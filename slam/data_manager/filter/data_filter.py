"""
Filter of dummy unrealistic measurements
"""
import logging
from slam.data_manager.factory.batch import DataBatch

from slam.utils.config import Config
from configs.paths.DEFAULT_FILE_PATHS import ConfigFilePaths


class RawDataFilter():
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.__params = Config(
            ConfigFilePaths.data_manager_config).attributes["data_filter"]

    def __filter_empty_messages(self) -> None:
        raise NotImplementedError()

    def __filter_extreme_values(self) -> None:
        raise NotImplementedError()

    def filter(self, batch: DataBatch) -> None:
        raise NotImplementedError()
