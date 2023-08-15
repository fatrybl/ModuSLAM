import logging
import sys
import psutil
from configs.paths.DEFAULT_FILE_PATHS import ConfigFilePaths
from slam import logger
from utils.config import Config

logger = logging.getLogger(__name__)


class MemoryAnalyzer():
    def __init__(self):
        self.__config = Config.from_file(
            ConfigFilePaths.data_manager_config.value)
        try:
            self.__graph_memory_percent = self.__config.attributes['memory_analyzer']['graph']
        except KeyError:
            logger.critical(
                f'"memory_analyzer.graph" params not found in {self.__config.file_path}')
            sys.exit(1)

    @property
    def total_memory(self):
        return psutil.virtual_memory().total

    @property
    def available_memory_percent(self):
        available_percent = (
            psutil.virtual_memory().available / self.total_memory) * 100
        return available_percent

    @property
    def used_memory_percent(self):
        return psutil.virtual_memory().percent

    @property
    def permissible_memory_percent(self):
        return 100 - self.__graph_memory_percent
