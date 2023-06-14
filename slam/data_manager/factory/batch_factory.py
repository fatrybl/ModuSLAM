import logging

from .batch import DataBatch
from .reader.data_reader import FileReader
from data_manager.memory_analyzer.memory_analyzer import MemoryAnalyzer
from utils.file_sorter import FileSorter
from collections import deque
from pathlib2 import Path
from utils.config import Config
from configs.paths.DEFAULT_FILE_PATHS import ConfigFilePaths
from utils.stopping_criterion import StoppingCriterion


class BatchFactory():
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.__config = Config(ConfigFilePaths.data_manager_config)
        self.__memory_analyzer = MemoryAnalyzer()
        self.__batch = DataBatch()
        self.__data_files = deque()
        self.__create_file_list()
        if self.__data_files:
            self.__file_reader = FileReader.create(self.__data_files[0])
        else:
            raise OSError('No data available')
        self.__current_file = None

    @property
    def batch(self) -> DataBatch:
        return self.__batch

    @property
    def data_files(self) -> deque:
        return self.__data_files

    def __create_file_list(self) -> None:
        self.__data_files = FileSorter.sort(
            Path(self.__config.attributes['data_dir']),
            self.__config.attributes['sort_key'])

    def __update_current_file(self) -> None:
        if self.__file_reader.is_file_processed:
            self.__data_files.popleft()

        if self.__data_files:
            self.__current_file = self.__data_files[0]
            self.__file_reader.is_file_processed = False
        else:
            self.__current_file = None
            print("All data files are processed")

    def __add_data(self) -> None:
        self.__update_current_file()
        if self.__current_file:
            new_element = self.__file_reader.get_element(self.__current_file)
            self.__batch += new_element
        else:
            StoppingCriterion.is_data_processed = True

    def create(self) -> None:
        while self.__memory_analyzer.used_percent < self.__memory_analyzer.allowed_percent and not StoppingCriterion.is_data_processed:
            self.__add_data()

    def delete(self) -> None:
        self.__batch = None

    def save(self) -> None:
        raise NotImplementedError
