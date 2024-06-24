import logging
from collections.abc import Sequence
from typing import overload

from plum import dispatch

from moduslam.data_manager.factory.batch import DataBatch
from moduslam.data_manager.factory.data_reader_ABC import DataReader
from moduslam.data_manager.factory.data_reader_factory import DataReaderFactory
from moduslam.data_manager.factory.element import Element
from moduslam.data_manager.memory_analyzer.memory_analyzer import MemoryAnalyzer
from moduslam.logger.logging_config import data_manager
from moduslam.setup_manager.sensors_factory.sensors import Sensor
from moduslam.system_configs.data_manager.batch_factory.batch_factory import (
    BatchFactoryConfig,
)
from moduslam.utils.auxiliary_dataclasses import PeriodicDataRequest
from moduslam.utils.stopping_criterion import StoppingCriterion

logger = logging.getLogger(data_manager)


class BatchFactory:
    """Factory for creating and managing data batch."""

    def __init__(self, cfg: BatchFactoryConfig) -> None:
        """
        Args:
            cfg: config with parameters for the Batch Factory.
        """

        self._memory_analyzer = MemoryAnalyzer(cfg.memory)
        self._data_reader: DataReader = DataReaderFactory.create_reader(cfg.dataset, cfg.regime)
        self._batch = DataBatch()

    @property
    def batch(self) -> DataBatch:
        """A data batch sorted by timestamps."""
        self._batch.sort()
        return self._batch

    @overload
    def create_batch(self) -> None:
        """
        @overload.

        Creates a new Data Batch from the dataset.
        """
        self.batch.clear()
        StoppingCriterion.state.data_processed = False
        print(f"Clearing batch...")
        print(f"Stopping Criterion: {StoppingCriterion.state.data_processed}")
        while not self._limitation():
            logger.info("Adding data to the batch using _ADD_DATA")
            self._add_data()

    @overload
    def create_batch(self, elements: Sequence[Element]) -> None:
        """
        @overload.

        Creates a new Data Batch for the collections of elements.

        Args:
            elements: sequence of elements w/o raw sensor measurements.
        """
        self.batch.clear()
        StoppingCriterion.state.data_processed = False
        for element in elements:
            self._add_data(element)

    @overload
    def create_batch(self, requests: set[PeriodicDataRequest]) -> None:
        """
        @overload.

        Creates a new Data Batch for the set of requests.

        Args:
            requests: set of requests to create a Data Batch.
        """
        self.batch.clear()
        StoppingCriterion.state.data_processed = False
        for request in requests:
            self._add_data(request)

    @dispatch
    def create_batch(self, elements=None):
        """
        @overload.

        Calls:
            1. Creates a new Data Batch from the dataset sequentially.
                Args:
                    __.

            2. Creates a new Data Batch from the collection of elements.
                Args:
                    elements (collection[Element]): collection of elements w/o raw sensor measurements.

            3. Creates a new Data Batch from the set of requests.
                Args:
                    requests (set[PeriodicDataRequest]): set of requests to create a Data Batch.
        """

    def save_batch(self) -> None:
        """Saves the Data Batch.\n Not implemented."""
        raise NotImplementedError

    @staticmethod
    def _set_stopping_criterion() -> None:
        """Sets the stopping criterion = True, when all data has been processed."""

        msg = "All data has been processed"
        logger.info(msg)
        StoppingCriterion.state.data_processed = True

    @staticmethod
    def _memory_limit_reached() -> None:
        """Changes the stopping criterion when the memory limit has been reached and
        logs the message."""

        msg = "Memory limit for Data Batch has been reached"
        logger.info(msg)
        StoppingCriterion.state.memory_limit = True

    def _limitation(self) -> bool:
        """Checks if any limitation has been reached to stop the creation of a new
        element for the Data Batch and returns stopping criterion status."""
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
            self._set_stopping_criterion()

    @overload
    def _add_data(self, no_data_element: Element) -> None:
        """
        @overload.

        Adds a new element to the Data Batch based on the requested Element w/o raw sensor measurement.

        Args:
            no_data_element: element w/o raw sensor measurement.
        """
        element_with_data: Element = self._data_reader.get_element(no_data_element)
        self._batch.add(element_with_data)

    @overload
    def _add_data(self, request: PeriodicDataRequest) -> None:
        """
        @overload.

        Adds a new element to the Data Batch based on the request.

        Attention: start/stop timestamps must be valid,
            exist in a dataset and correspond to real measurements.

        Args:
            request: sensor and time range of measurements to be added to the Data Batch.

        Raises:
            StopIteration: if the element for the given sensor and "start" timestamp does not exist.
        """
        exception_msg: str = f"Can not fulfil the request {request}. Check sensor and time range."

        start: int = request.period.start
        stop: int = request.period.stop
        sensor: Sensor = request.sensor

        try:
            first_element: Element = self._data_reader.get_element(sensor, start)
        except StopIteration:
            logger.error(exception_msg)
            raise StopIteration(exception_msg)

        self._batch.add(first_element)

        current_timestamp: int = first_element.timestamp

        if current_timestamp != stop:
            while current_timestamp < stop:
                element: Element | None = self._data_reader.get_element(sensor)
                if element is None:
                    logger.error(exception_msg)
                    raise StopIteration(exception_msg)
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
            1. Adds new element to the DataBatch.
                Args:
                    __.

            2. Adds a new element to the Data Batch based on the requested Element w/o raw sensor measurement.
                Args:
                    no_data_element (Element): element w/o raw sensor measurement.

            3. Adds a new element to the Data Batch based on the request.
                Args:
                    request (PeriodicDataRequest): sensor and time range of measurements to be added to the Data Batch.
        """
