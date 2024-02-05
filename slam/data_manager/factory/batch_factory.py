import logging
from collections import deque
from typing import overload

from plum import dispatch

from configs.system.data_manager.batch_factory.batch_factory import BatchFactoryConfig
from slam.data_manager.factory.batch import DataBatch
from slam.data_manager.factory.readers.data_reader_ABC import DataReader
from slam.data_manager.factory.readers.data_reader_factory import DataReaderFactory
from slam.data_manager.factory.readers.element_factory import Element
from slam.data_manager.memory_analyzer.memory_analyzer import MemoryAnalyzer
from slam.setup_manager.sensor_factory.sensors import Sensor
from slam.utils.auxiliary_dataclasses import PeriodicData
from slam.utils.stopping_criterion import StoppingCriterion

logger = logging.getLogger(__name__)


class BatchFactory:
    """Creates and manages Data Batch."""

    def __init__(self, cfg: BatchFactoryConfig) -> None:
        """
        Args:
            cfg (DataManagerConfig): config with parameters
        """
        self._break_point = StoppingCriterion
        self._memory_analyzer = MemoryAnalyzer(cfg.memory)
        self._batch = DataBatch()
        reader: type[DataReader] = DataReaderFactory.get_reader(cfg.dataset.reader)
        self._data_reader: DataReader = reader(cfg.dataset, cfg.regime)

    @property
    def batch(self) -> DataBatch:
        """
        Returns:
            DataBatch: Sorted Data Batch by timestamp.
        """
        self._batch.sort()
        return self._batch

    def __data_processed(self) -> None:
        """
        Called when all data has been processed. Turns ON global Stopping Criterion.
        """

        msg = "All data has been processed"
        logger.info(msg)
        self._break_point.state.is_data_processed = True

    def __memory_limit_reached(self) -> None:
        """
        Called when the memory limit for a batch has been reached. Turns ON global Stopping Criterion.
        """

        msg = "Memory limit for Data Batch has been reached"
        logger.info(msg)
        self._break_point.state.is_memory_limit = True

    def __limitation(self) -> bool:
        """
        Checks if any limitation has been reached to stop the creation of a new element for the Data Batch.

        Returns:
            bool: state of the Stopping Criterion singleton
        """
        used_memory: float = self._memory_analyzer.used_memory_percent
        permissible_memory: float = self._memory_analyzer.permissible_memory_percent

        if used_memory > permissible_memory:
            self.__memory_limit_reached()

        return self._break_point.is_active()

    @overload
    def _add_data(self) -> None:
        """
        @overload.
        Adds new element to the DataBatch.
        """
        new_element: Element | None = self._data_reader.get_element()
        if new_element:
            self._batch.add(new_element)
        else:
            self.__data_processed()

    @overload
    def _add_data(self, no_data_element: Element) -> None:
        """
        @overload.
        Adds a new element to the Data Batch based on the requested Element
        w/o raw sensor measurement.

        Args:
            no_data_element (Element): element w/o raw sensor measurement.
        """
        element_with_data: Element = self._data_reader.get_element(no_data_element)
        self._batch.add(element_with_data)

    @overload
    def _add_data(self, request: PeriodicData) -> None:
        """
        @overload.
        Adds a new element to the Data Batch based on the request.
        Assumption: start/stop timestamps must be valid, exist in a dataset and correspond to real measurements.

        Args:
            request (PeriodicData): contains sensor and time range (start, stop)
            of measurements to be added to the Data Batch.
        """
        start: int = request.period.start
        stop: int = request.period.stop
        sensor: Sensor = request.sensor

        first_element: Element = self._data_reader.get_element(sensor, start)
        self._batch.add(first_element)
        current_timestamp: int = first_element.timestamp
        if start != stop:
            while current_timestamp < stop:
                element: Element = self._data_reader.get_element(sensor)
                self._batch.add(element)
                current_timestamp = element.timestamp

    @dispatch
    def _add_data(self, element=None):
        """
        @overload.

        Calls:
            1. add new element to the data batch.

            2. add new element to the data batch based on the requested element.
                Args:
                    element (Element): element w/o raw sensor measurement.

            3. add new element to the data batch based on the request.
                Args:
                    request (PeriodicData): contains sensor and time range (start, stop)
                    of measurements to be added to the Data Batch.
        """

    @overload
    def create_batch(self) -> None:
        """
        @overload.
        Creates a new Data Batch from the dataset.
        """
        self.batch.clear()
        self._break_point.state.is_data_processed = False
        while not self.__limitation():
            self._add_data()

    @overload
    def create_batch(self, elements: deque[Element]) -> None:
        """
        @overload.
        Creates a new Data Batch from the deque of elements.

        Args:
            elements (deque[Element]): deque of elements w/o raw sensor measurements.
        """
        self.batch.clear()
        self._break_point.state.is_data_processed = False
        for element in elements:
            self._add_data(element)

    @overload
    def create_batch(self, requests: set[PeriodicData]) -> None:
        """
        @overload.
        Creates a new Data Batch from the set of requests.

        Args:
            requests (set[PeriodicData]): each request contains sensor and time range (start, stop)
            of measurements to be added to the Data Batch
        """
        self.batch.clear()
        self._break_point.state.is_data_processed = False
        for request in requests:
            self._add_data(request)

    @dispatch
    def create_batch(self, elements=None):
        """
        @overload.

        Calls:
            1. create a new Data Batch from the dataset sequentially.
            2. create a new Data Batch from the deque of elements.
                Args:
                    elements (deque[Element]): deque of elements w/o raw sensor measurements.
            3. create a new Data Batch from the set of requests.
                Args:
                    requests (set[PeriodicData]): each request contains sensor and time range (start, stop)
                    of measurements to be added to the Data Batch
        """

    def save_batch(self) -> None:
        """
        Saves the Data Batch to the disk.
        Not implemented yet.
        """
        raise NotImplementedError
