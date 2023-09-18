import logging

from plum import dispatch
from typing import Type

from slam.data_manager.factory.batch import DataBatch
from slam.data_manager.factory.readers.data_reader import DataReader
from slam.data_manager.factory.readers.data_reader_factory import DataReaderFactory
from slam.data_manager.memory_analyzer.memory_analyzer import MemoryAnalyzer
from slam.utils.stopping_criterion import StoppingCriterionSingleton
from slam.data_manager.factory.readers.element_factory import Element

logger = logging.getLogger(__name__)


class BatchFactory():
    def __init__(self) -> None:
        self._memory_analyzer = MemoryAnalyzer()
        self._batch = DataBatch()
        self._data_reader: Type[DataReader] = DataReaderFactory()
        self._break_point = StoppingCriterionSingleton()

    @property
    def batch(self) -> DataBatch:
        return self._batch

    @batch.deleter
    def batch(self) -> None:
        del self._batch

    @dispatch
    def _add_data(self) -> None:
        new_element: Element = self._data_reader.get_element()
        if new_element:
            self._batch.add(new_element)
        else:
            logger.info("All data has been processed")
            self._break_point.is_data_processed = True

    @dispatch
    def _add_data(self, element_no_data: Element) -> None:
        element_with_data: Element = self._data_reader.get_element(
            element_no_data)
        self._batch.add(element_with_data)

    @dispatch
    def create_batch(self) -> None:
        while not self.__limitation():
            self._add_data()

    @dispatch
    def create_batch(self, measurements: list[Element]) -> None:
        for m in measurements:
            self._add_data(m)

    def __limitation(self) -> bool:
        used_memory: float = self._memory_analyzer.used_memory_percent
        permissible_memory: float = self._memory_analyzer.permissible_memory_percent

        if used_memory > permissible_memory:
            self._break_point.is_memory_limit = True
            logger.info("Memory limit for Data Batch has been reached")
            return True

        if self._break_point.is_data_processed:
            return True

        else:
            return False

    def save_batch(self) -> None:
        raise NotImplementedError
