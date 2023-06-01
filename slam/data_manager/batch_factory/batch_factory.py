import logging
from data_batch import DataBatch
from data_reader.data_reader import DataReader
from data_manager.memory_analyzer.memory_analyzer import MemoryAnalyzer


class BatchFactory():
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.__memory_analyzer = MemoryAnalyzer()
        self.__batch = DataBatch()
        self.__data_reader = DataReader()
        self.__data_files = []
        self.__current_file = None
        self.current_batch_position = None

    @property
    def batch(self) -> DataBatch:
        return self.__batch

    def __add_data(self):
        new_row = self.__data_reader.get_row()
        self.__batch += new_row

    def create(self) -> None:
        while self.__memory_analyzer.used_percent <= self.__memory_analyzer.allowed_percent:
            self.__add_data()

    def delete(self) -> None:
        pass

    def save(self) -> None:
        pass
