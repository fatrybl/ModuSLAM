import logging

from slam.data_manager.factory.batch import DataBatch
from slam.data_manager.factory.readers.data_reader_factory import DataReaderFactory
from slam.data_manager.memory_analyzer.memory_analyzer import MemoryAnalyzer
from slam.utils.stopping_criterion import StoppingCriterionSingleton

logger = logging.getLogger(__name__)


class BatchFactory():
    def __init__(self) -> None:
        self.__memory_analyzer = MemoryAnalyzer()
        self.__batch = DataBatch()
        self.__data_reader = DataReaderFactory()
        self.__break_point = StoppingCriterionSingleton()

    @property
    def batch(self) -> DataBatch:
        return self.__batch

    def __add_data(self) -> None:
        new_element = self.__data_reader.get_element()
        if new_element:
            self.__batch.add(new_element)
        else:
            logger.info("All data has been processed")
            self.__break_point.is_data_processed = True

    def __limitation(self) -> bool:
        used_memory = self.__memory_analyzer.used_memory_percent
        permissible_memory = self.__memory_analyzer.permissible_memory_percent
        if (used_memory < permissible_memory and not self.__break_point.is_data_processed):
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
