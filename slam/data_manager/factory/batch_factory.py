import logging
from collections.abc import Sequence
from typing import overload

from plum import dispatch

from slam.data_manager.factory.batch import DataBatch
from slam.data_manager.factory.data_reader_ABC import DataReader
from slam.data_manager.factory.data_reader_factory import DataReaderFactory
from slam.data_manager.factory.element import Element
from slam.data_manager.memory_analyzer.memory_analyzer import MemoryAnalyzer
from slam.setup_manager.sensors_factory.sensors import Sensor
from slam.system_configs.system.data_manager.batch_factory.batch_factory import (
    BatchFactoryConfig,
)
from slam.utils.auxiliary_dataclasses import PeriodicData
from slam.utils.stopping_criterion import StoppingCriterion

logger = logging.getLogger(__name__)


class BatchFactory:
    """Factory for creating and managing a data batch."""

    def __init__(self, cfg: BatchFactoryConfig) -> None:
        """
        Args:
            cfg (DataManagerConfig): config with parameters
        """

        self._memory_analyzer = MemoryAnalyzer(cfg.memory)
        self._data_reader: DataReader = DataReaderFactory.get_reader(cfg.dataset, cfg.regime)
        self._batch = DataBatch()

    @property
    def batch(self) -> DataBatch:
        """A data batch sorted by timestamp.

        Returns:
            (DataBatch): a data batch sorted by timestamp.
        """
        self._batch.sort()
        return self._batch

    @staticmethod
    def _data_processed() -> None:
        """Called when all data has been processed.

        Turns ON global Stopping Criterion.
        """

        msg = "All data has been processed"
        logger.info(msg)
        StoppingCriterion.state.is_data_processed = True

    @staticmethod
    def _memory_limit_reached() -> None:
        """Called when the memory limit for a batch has been reached.

        Turns ON global Stopping Criterion.
        """

        msg = "Memory limit for Data Batch has been reached"
        logger.info(msg)
        StoppingCriterion.state.is_memory_limit = True

    def _limitation(self) -> bool:
        """Checks if any limitation has been reached to stop the creation of a new
        element for the Data Batch.

        Returns:
            bool: state of the Stopping Criterion.
        """
        used_memory: float = self._memory_analyzer.used_memory_percent
        permissible_memory: float = self._memory_analyzer.permissible_memory_percent

        if used_memory > permissible_memory:
            self._memory_limit_reached()

        return StoppingCriterion.is_active()

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
            self._data_processed()

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

        Attention: start/stop timestamps must be valid,
            exist in a dataset and correspond to real measurements.

        Args:
            request (PeriodicData): contains sensor and time range (start, stop)
            of measurements to be added to the Data Batch.

        Raises:
            StopIteration: if the element for the given sensor and "start" timestamp does not exist.
            ValueError: if the element for the given sensor and "stop" timestamp does not exist.
        """
        exception_msg: str = f"Can not fulfil the request {request}. Check sensor and timestamps."
        exception: Exception = StopIteration(exception_msg)

        start: int = request.period.start
        stop: int = request.period.stop
        sensor: Sensor = request.sensor

        try:
            first_element: Element = self._data_reader.get_element(sensor, start)
        except StopIteration:
            logger.error(exception_msg)
            raise exception

        self._batch.add(first_element)

        current_timestamp: int = first_element.timestamp

        if current_timestamp != stop:
            while current_timestamp < stop:
                element: Element | None = self._data_reader.get_element(sensor)
                if element is None:
                    logger.error(exception_msg)
                    raise exception
                else:
                    current_timestamp = element.timestamp
                    if current_timestamp <= stop:
                        self._batch.add(element)
                    else:
                        break

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
        StoppingCriterion.state.is_data_processed = False
        while not self._limitation():
            self._add_data()

    @overload
    def create_batch(self, elements: Sequence[Element]) -> None:
        """
        @overload.
        Creates a new Data Batch from the collections of elements.

        Args:
            elements (Sequence[Element]): sequence of elements w/o raw sensor measurements.
        """
        self.batch.clear()
        StoppingCriterion.state.is_data_processed = False
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
        StoppingCriterion.state.is_data_processed = False
        for request in requests:
            self._add_data(request)

    @dispatch
    def create_batch(self, elements=None):
        """
        @overload.

        Calls:
            1. Create a new Data Batch from the dataset sequentially.
                Args:
                    None.

            2. Create a new Data Batch from the collection of elements.
                Args:
                    elements (collection[Element]): collection of elements w/o raw sensor measurements.

            3. Create a new Data Batch from the set of requests.
                Args:
                    requests (set[PeriodicData]): each request contains sensor
                    and time range (start, stop) of measurements to be added to the Data Batch
        """

    def save_batch(self) -> None:
        """Saves the Data Batch to the disk.

        Not implemented yet.
        """
        raise NotImplementedError
