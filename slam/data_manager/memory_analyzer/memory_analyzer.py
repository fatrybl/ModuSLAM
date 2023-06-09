import psutil
from configs.paths.DEFAULT_FILE_PATHS import ConfigFilePaths
from utils.config import Config


class MemoryAnalyzer():
    DEFAULT_MEMORY_PERCENT = 0.5

    def __init__(self):
        self.__config = Config(ConfigFilePaths.data_manager_config)
        self.__total_memory = psutil.virtual_memory().total
        self.__available_memory = psutil.virtual_memory().available
        self.__used_memory_percent = psutil.virtual_memory().percent
        self.__allowed_memory_percent = self.__config.attributes.batch_memory_percent

    @property
    def total_memory(self):
        return self.__total_memory

    @property
    def available_memory_percent(self):
        return self.__available_memory

    @property
    def used_memory_percent(self):
        return self.__used_memory_percent

    @property
    def allowed_memory_percent(self):
        return self.__allowed_memory_percent
