import logging
from typing import Type

from plum import dispatch

from slam.data_manager.factory.batch import DataBatch
from slam.data_manager.factory.readers.data_reader import DataReader
from slam.data_manager.factory.readers.data_reader_factory import DataReaderFactory
from slam.data_manager.memory_analyzer.memory_analyzer import MemoryAnalyzer
from slam.setup_manager.sensor_factory.sensors import Sensor
from slam.utils.auxiliary_dataclasses import PeriodicData
from slam.utils.stopping_criterion import StoppingCriterionSingleton
from slam.data_manager.factory.readers.element_factory import Element
from configs.system.data_manager.manager import DataManager as DataManagerConfig

logger = logging.getLogger(__name__)


class BatchFactory():
    """Creates and manages Data Batch.
    """

    def __init__(self, cfg: DataManagerConfig) -> None:
        self._break_point = StoppingCriterionSingleton()
        self._memory_analyzer = MemoryAnalyzer(cfg.memory)
        self._batch = DataBatch()
        self._data_reader: Type[DataReader] = DataReaderFactory(
            cfg.dataset,
            cfg.regime)

    @property
    def batch(self) -> DataBatch:
        return self._batch

    @batch.deleter
    def batch(self) -> None:
        del self._batch

    def __data_processed(self) -> None:
        """Called when all data has been processed. Turns ON global Stopping Criterion."""

        msg = "All data has been processed"
        logger.info(msg)
        self._break_point.is_data_processed = True

    def __memory_limit_reached(self) -> None:
        """Called when the memory limit for a batch has been reached. Turns ON global Stopping Criterion."""

        msg = "Memory limit for Data Batch has been reached"
        logger.info(msg)
        self._break_point.is_memory_limit = True

    def __limitation(self) -> bool:
        """Checks if any limitation has been reached to stop the creation of a new element for the Data Batch. 

        Returns:
            bool: state of the Stopping Criterion singleton
        """
        used_memory: float = self._memory_analyzer.used_memory_percent
        permissible_memory: float = self._memory_analyzer.permissible_memory_percent

        if used_memory > permissible_memory:
            self.__memory_limit_reached()

        return self._break_point.ON

    @dispatch
    def _add_data(self) -> None:
        """Adds new element to the Data Batch."""

        new_element: Element = self._data_reader.get_element()
        if new_element:
            self._batch.add(new_element)
        else:
            self.__data_processed()

    @dispatch
    def _add_data(self, no_data_element: Element) -> None:
        """Adds a new element to the Data Batch based on the requested Element 
        w/o raw sensor measurement.

        Args:
            no_data_element (Element): element w/o raw sensor measurement.
        """
        element_with_data: Element = self._data_reader.get_element(
            no_data_element)
        self._batch.add(element_with_data)

    @dispatch
    def _add_data(self, request: PeriodicData) -> None:
        """Adds a new element to the Data Batch based on the request.

        Args:
            request (PeriodicData): contains sensor and time range (start, stop) 
            of measurements to be added to the Data Batch.
        """
        start: int = request.period.start
        stop: int = request.period.stop
        sensor: Type[Sensor] = request.sensor

        first_element: Element = self._data_reader.get_element(
            sensor, init_time=start)
        self._batch.add(first_element)
        current_timestamp: int = first_element.timestamp

        if start != stop:
            while current_timestamp < stop:
                element: Element = self._data_reader.get_element(sensor)
                self._batch.add(element)
                current_timestamp = element.timestamp

    @dispatch
    def create_batch(self) -> None:
        """Creates a new Data Batch from the dataset.
        """
        while not self.__limitation():
            self._add_data()

    @dispatch
    def create_batch(self, elements: list[Element]) -> None:
        """Creates a new Data Batch from the list of elements.

        Args:
            elements (list[Element]): list of elements w/o raw sensor measurements.
        """
        for element in elements:
            self._add_data(element)

    @dispatch
    def create_batch(self, requests: set[PeriodicData]) -> None:
        """Creates a new Data Batch from the set of requests.

        Args:
            requests (set[PeriodicData]): each request contains sensor and time range (start, stop) 
            of measurements to be added to the Data Batch
        """
        for request in requests:
            self._add_data(request)

    def save_batch(self) -> None:
        raise NotImplementedError
