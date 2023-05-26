import logging
from data_batch import DataBatch
from data_reader.data_reader import DataReader
from data_manager.memory_analyzer.memory_analyzer import MemoryAnalyzer


class BatchFactory():
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.__memory_analyzer = MemoryAnalyzer()
        self.__batch = DataBatch()
        self.__data_files = []
        self.__current_file = None
        self.isEmpty = True
        self.current_batch_position = None

    @property
    def batch(self) -> DataBatch:
        return self.__batch

    def create_batch(self) -> None:
        while self.__memory_analyzer.used_memory_percent <= self.__memory_analyzer.allowed_memory_percent:
            self.__batch.add_data()
        
        self.isEmpty = False

    def delete_batch(self) -> None:
        pass

    def save_batch(self) -> None:
        pass
