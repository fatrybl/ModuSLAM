import logging

from data_batch import DataBatch
from data_reader.data_reader import FileReader
from data_manager.memory_analyzer.memory_analyzer import MemoryAnalyzer
from collections import deque
from pathlib2 import Path


class BatchFactory():
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.__memory_analyzer = MemoryAnalyzer()
        self.__batch = DataBatch()
        self.__file_reader = FileReader()
        self.__data_files = deque()
        self.current_batch_position = None

    @property
    def batch(self) -> DataBatch:
        return self.__batch

    def __add_data(self, file):
        new_row = self.__file_reader.get_row(file)
        self.__batch += new_row

    def create(self) -> None:
        while self.__data_files and self.__memory_analyzer.used_percent <= self.__memory_analyzer.allowed_percent:
            try:
                self.__add_data(file)
                self.__data_files.popleft()
            except Exception as e:
                pass

    def delete(self) -> None:
        del self.__batch

    def save(self) -> None:
        pass
