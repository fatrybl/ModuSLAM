import logging

from .batch import DataBatch
from .readers.data_reader_factory import DataReaderFactory
from data_manager.memory_analyzer.memory_analyzer import MemoryAnalyzer
from utils.stopping_criterion import StoppingCriterion


class BatchFactory():
    logger = logging.getLogger(__name__)

    def __init__(self) -> None:
        self.__memory_analyzer = MemoryAnalyzer()
        self.__batch = DataBatch()
        self.__data_reader = DataReaderFactory()

    @property
    def batch(self) -> DataBatch:
        return self.__batch

    def __add_data(self) -> None:
        self.__data_reader.get_element()
        new_element = self.__data_reader.element
        if new_element:
            self.__batch.add(new_element)
        else:
            StoppingCriterion.is_data_processed = True

    def __limitation(self) -> bool:
        used_memory = self.__memory_analyzer.used_memory_percent
        permissible_memory = self.__memory_analyzer.permissible_memory_percent
        if (used_memory < permissible_memory and not StoppingCriterion.is_data_processed):
            return False
        else:
            return True

    def create_batch(self) -> None:
        while not self.__limitation():
            self.__add_data()

    def delete_batch(self) -> None:
        self.__batch = None

    def create_batch_from_measurements(self) -> None:
        raise NotImplementedError

    def save_batch(self) -> None:
        raise NotImplementedError
