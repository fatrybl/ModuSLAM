import psutil
from configs.paths.DEFAULT_FILE_PATHS import ConfigFilePaths
from utils.config import Config


class MemoryAnalyzer():
    def __init__(self):
        self.__config = Config(ConfigFilePaths.data_manager_config)
        self.__graph_memory_percent = self.__config.attributes['memory_analyzer']['graph']

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
