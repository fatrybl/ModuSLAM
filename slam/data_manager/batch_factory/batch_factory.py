import logging

from data_batch import DataBatch
from data_reader.data_reader import FileReader
from data_manager.memory_analyzer.memory_analyzer import MemoryAnalyzer
from collections import deque


class BatchFactory():
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.__memory_analyzer = MemoryAnalyzer()
        self.__batch = DataBatch()
        self.__file_reader = FileReader()
        self.__data_files = deque()
        self.__current_file = None

    @property
    def batch(self) -> DataBatch:
        return self.__batch

    @property
    def data_files(self) -> deque:
        return self.__data_files

    @data_files.setter
    def data_files(self, value: deque):
        assert value is not None
        self.__data_files = value

    def __update_current_file(self) -> None:
        if self.__file_reader.is_file_processed:
            self.__data_files.popleft()
        if self.__data_files:
            self.__current_file = self.__data_files[0]
            self.__file_reader.is_file_processed = False
        else:
            raise Exception("All data files are processed")

    def __add_data(self) -> None:
        self.__update_current_file()
        new_element = self.__file_reader.get_element(self.__current_file)
        self.__batch += new_element

    def create(self) -> None:
        while self.__memory_analyzer.used_percent <= self.__memory_analyzer.allowed_percent:
            try:
                self.__add_data()
            except Exception as e:
                pass

    def delete(self) -> None:
        del self.__batch

    def save(self) -> None:
        pass
