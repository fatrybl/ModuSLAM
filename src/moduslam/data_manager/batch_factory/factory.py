import logging
from collections.abc import Sequence

from src.logger.logging_config import data_manager
from src.moduslam.data_manager.batch_factory.batch import DataBatch, Element
from src.moduslam.data_manager.batch_factory.configs import BatchFactoryConfig
from src.moduslam.data_manager.batch_factory.data_readers.reader_ABC import DataReader
from src.moduslam.data_manager.batch_factory.data_readers.reader_factory import create
from src.moduslam.data_manager.memory_analyzer import MemoryAnalyzer
from src.moduslam.sensors_factory.factory import SensorsFactory
from src.utils.auxiliary_dataclasses import PeriodicDataRequest
from src.utils.exceptions import StateNotSetError, UnfeasibleRequestError

logger = logging.getLogger(data_manager)


class BatchFactory:
    """Factory for creating and managing data batch."""

    def __init__(self, config: BatchFactoryConfig) -> None:
        self._all_data_processed = False
        self._batch = DataBatch()
        self._memory_analyzer = MemoryAnalyzer(config.batch_memory_percent)
        self._data_reader, regime = create(config.dataset, config.regime)
        sensors = SensorsFactory.get_sensors()
        self._data_reader.configure(regime, sensors)

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

        self._sort_if_needed()

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

        self._sort_if_needed()

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

        self._sort_if_needed()

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

    def _sort_if_needed(self) -> None:
        """Sorts the batch if needed."""
        if not self._batch.is_sorted:
            logger.warning("The batch is not sorted by timestamp. Sorting it now.")
            self._batch.sort()
