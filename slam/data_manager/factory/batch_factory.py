import logging

from .batch import DataBatch
from .readers.data_reader_factory import DataReaderFactory
from data_manager.memory_analyzer.memory_analyzer import MemoryAnalyzer
from utils.stopping_criterion import StoppingCriterion


class BatchFactory():
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.__memory_analyzer = MemoryAnalyzer()
        self.__batch = DataBatch()
        self.__data_reader = DataReaderFactory()

    @property
    def batch(self) -> DataBatch:
        return self.__batch

    def __add_data(self) -> None:
        new_element = self.__data_reader.get_element()
        self.__batch.add(new_element)

    def __is_criteria(self,):
        if (self.__memory_analyzer.used_memory_percent < self.__memory_analyzer.allowed_memory_percent and
                not StoppingCriterion.is_data_processed):
            return True
        else:
            return False

    def create_batch(self) -> None:
        while self.__is_criteria():
            self.__add_data()

    def delete_batch(self) -> None:
        self.__batch = None

    def save_batch(self) -> None:
        raise NotImplementedError
