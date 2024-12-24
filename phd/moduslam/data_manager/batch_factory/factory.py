import logging
from collections.abc import Sequence

from phd.logger.logging_config import data_manager
from phd.moduslam.data_manager.batch_factory.batch import DataBatch, Element
from phd.moduslam.data_manager.batch_factory.configs import BatchFactoryConfig
from phd.moduslam.data_manager.batch_factory.readers.reader_ABC import DataReader
from phd.moduslam.data_manager.batch_factory.readers.reader_factory import (
    DataReaderFactory,
)
from phd.moduslam.data_manager.memory_analyzer import MemoryAnalyzer
from phd.utils.auxiliary_dataclasses import PeriodicDataRequest
from phd.utils.exceptions import StateNotSetError, UnfeasibleRequestError

logger = logging.getLogger(data_manager)


class BatchFactory:
    """Factory for creating and managing data batch."""

    def __init__(self, config: BatchFactoryConfig) -> None:
        self._all_data_processed: bool = False
        self._batch = DataBatch()
        self._memory_analyzer = MemoryAnalyzer(config.batch_memory_percent)
        self._data_reader = DataReaderFactory.create(config.dataset, config.regime)

    @property
    def batch(self) -> DataBatch:
        """A data batch."""
        return self._batch

    def fill_batch_sequentially(self) -> None:
        """Adds elements with raw sensor measurements to the batch sequentially from the
        dataset."""

        with self._data_reader as reader:
            while not self._all_data_processed:

                self._check_memory()
                element = reader.get_next_element()

                if element:
                    self._batch.add(element)
                else:
                    self._all_data_processed = True
                    logger.info("All data in the dataset has been processed.")

        self._batch.sort()

    def fill_batch_with_elements(self, elements: Sequence[Element]) -> None:
        """Adds elements with raw sensor measurements to the batch for the given
        elements w/o raw measurements.

        Args:
            elements: sequence of elements w/o raw sensor measurements.
        """

        elements = sorted(elements, key=lambda x: x.timestamp)

        with self._data_reader as reader:
            for empty_element in elements:

                self._check_memory()
                element = reader.get_element(empty_element)
                self._batch.add(element)

        self._batch.sort()

    def fill_batch_by_request(self, request: PeriodicDataRequest) -> None:
        """Adds elements with raw sensor measurements to the batch for the given
        request.

        Args:
            request: sequence of requests to create a Data Batch.

        Raises:
            UnfeasibleRequestError: can not fulfill the request.
        """

        with self._data_reader as reader:

            elements = self._fulfill_request(reader, request)

            if elements:
                for el in elements:
                    self._batch.add(el)
            else:
                msg = f"Can not fulfill the request {request}."
                logger.error(msg)
                raise UnfeasibleRequestError(msg)

        self._batch.sort()

    def _fulfill_request(
        self, reader: DataReader, request: PeriodicDataRequest
    ) -> list[Element] | None:
        """Gets requested elements.

        Args:
            request: a request with the sensor and margin timestamps .

        Returns:
            list of elements or None.
        """
        sensor = request.sensor
        start, stop = request.period.start, request.period.stop
        elements: list[Element] = []
        current_timestamp: int = -1

        try:
            reader.set_initial_state(sensor, start)
        except StateNotSetError:
            return None

        while current_timestamp < stop:

            self._check_memory()
            element = reader.get_next_element(sensor)

            if element:
                elements.append(element)
                current_timestamp = element.timestamp
            else:
                logger.error(
                    f"Can not get the next element for sensor {sensor}. "
                    f"Previous timestamp: {current_timestamp}."
                )
                return None

        return elements

    def _check_memory(self) -> None:
        """Checks if the memory limit is exceeded.

        Raises:
            MemoryError: memory limit is exceeded.
        """
        msg = "Memory limit is exceeded."
        if not self._memory_analyzer.enough_memory:
            logger.error(msg)
            raise MemoryError(msg)
