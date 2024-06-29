import logging
from collections.abc import Sequence
from typing import overload

from plum import dispatch

from moduslam.data_manager.batch_factory.batch import DataBatch
from moduslam.data_manager.batch_factory.element import Element
from moduslam.data_manager.batch_factory.readers.data_reader_ABC import DataReader
from moduslam.data_manager.batch_factory.readers.data_reader_factory import (
    DataReaderFactory,
)
from moduslam.data_manager.memory_analyzer.memory_analyzer import MemoryAnalyzer
from moduslam.logger.logging_config import data_manager
from moduslam.system_configs.data_manager.batch_factory.batch_factory import (
    BatchFactoryConfig,
)
from moduslam.utils.auxiliary_dataclasses import PeriodicDataRequest
from moduslam.utils.exceptions import ItemNotFoundError, UnfeasibleRequestError

logger = logging.getLogger(data_manager)


class BatchFactory:
    """Factory for creating and managing data batch."""

    def __init__(self, config: BatchFactoryConfig) -> None:
        """
        Args:
            config: config with parameters for the Batch Factory.
        """
        self._batch = DataBatch()
        self._memory_analyzer = MemoryAnalyzer(config.batch_memory_percent)
        self._data_reader = DataReaderFactory.create(config.dataset, config.regime)
        self._all_data_processed: bool = False

    @property
    def batch(self) -> DataBatch:
        """A data batch sorted by timestamps."""
        self._batch.sort()
        return self._batch

    @overload
    def create_batch(self) -> None:
        """
        @overload.

        Creates sequentially a new Data Batch from the dataset.

        Raises:
            MemoryError: memory limit exceeded.
        """
        self._batch.clear()

        with self._data_reader as reader:
            while not self._all_data_processed:

                self._check_memory()
                element = reader.get_next_element()

                if element:
                    self._batch.add(element)
                else:
                    self._all_data_processed = True
                    msg = "All data in the dataset has been processed."
                    logger.info(msg)

    @overload
    def create_batch(self, elements: Sequence[Element]) -> None:
        """@overload.

        Creates a new Data Batch for the sequence of elements.

        Args:
            elements: sequence of elements w/o raw sensor measurements.

        Raises:
            MemoryError: memory limit exceeded.
        """
        self._batch.clear()

        elements = sorted(elements, key=lambda x: x.timestamp)

        with self._data_reader as reader:
            for empty_element in elements:

                self._check_memory()
                element = reader.get_element(empty_element)
                self._batch.add(element)

    @overload
    def create_batch(self, request: PeriodicDataRequest) -> None:
        """@overload.

        Creates a new Data Batch for the sequence of requests.

        Args:
            request: sequence of requests to create a Data Batch.

        Raises:
            UnfeasibleRequestError: can not fulfill the request.

            MemoryError.
        """
        self._batch.clear()

        with self._data_reader as reader:
            elements = self._fulfill_request(reader, request)

            if elements:
                for el in elements:
                    self._batch.add(el)
            else:
                msg = f"Can not fulfill the request {request}."
                logger.error(msg)
                raise UnfeasibleRequestError(msg)

    @dispatch
    def create_batch(self, elements=None):
        """@overload.

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

    def _fulfill_request(
        self, reader: DataReader, request: PeriodicDataRequest
    ) -> list[Element] | None:
        """Gets requested elements.

        Args:
            request: a request with the sensor and margin timestamps .

        Returns:
            list of elements or None.

        Raises:
            MemoryError: memory limit exceeded.
        """
        sensor = request.sensor
        start, stop = request.period.start, request.period.stop
        elements = []
        current_timestamp = -1

        try:
            reader.set_initial_state(sensor, start)
        except ItemNotFoundError:
            msg = f"Can not set the initial state for sensor {sensor} at {start}."
            logger.error(msg)
            return None

        while current_timestamp < stop:

            self._check_memory()
            element = reader.get_next_element(sensor)

            if element:
                elements.append(element)
                current_timestamp = element.timestamp
            else:
                msg = f"Can not get the next element for sensor {sensor}. Previous timestamp: {current_timestamp}."
                logger.error(msg)
                return None

        return elements

    def _check_memory(self) -> None:
        """Checks if the memory limit is exceeded.

        Raises:
            MemoryError: memory limit exceeded.
        """
        if not self._memory_analyzer.enough_memory:
            msg = "Memory limit exceeded."
            logger.error(msg)
            raise MemoryError(msg)
