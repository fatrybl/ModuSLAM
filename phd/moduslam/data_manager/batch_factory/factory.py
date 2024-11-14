import logging
from collections.abc import Sequence

from hydra import compose, initialize
from hydra.core.config_store import ConfigStore

from phd.logger.logging_config import data_manager
from phd.moduslam.data_manager.batch_factory.base_configs import BatchFactoryConfig
from phd.moduslam.data_manager.batch_factory.batch import DataBatch, Element
from phd.moduslam.data_manager.batch_factory.memory_analyzer import MemoryAnalyzer
from phd.moduslam.data_manager.batch_factory.readers.data_reader_ABC import DataReader
from phd.moduslam.data_manager.batch_factory.readers.data_reader_factory import (
    DataReaderFactory,
)
from phd.moduslam.data_manager.batch_factory.readers.kaist.config_objects.base import (
    KaistConfig,
)
from phd.moduslam.data_manager.batch_factory.readers.tum_vie.config_objects.base import (
    TumVieConfig,
)
from phd.moduslam.utils.auxiliary_dataclasses import PeriodicDataRequest
from phd.moduslam.utils.exceptions import ItemNotFoundError, UnfeasibleRequestError

logger = logging.getLogger(data_manager)


def register_configs():
    cs = ConfigStore.instance()
    cs.store(name="base_factory", node=BatchFactoryConfig)
    cs.store(name="base_kaist_urban_dataset", node=KaistConfig)
    cs.store(name="base_tum_vie_dataset", node=TumVieConfig)


register_configs()


class BatchFactory:
    """Factory for creating and managing data batch."""

    def __init__(self) -> None:
        self._all_data_processed: bool = False
        self._batch = DataBatch()

        with initialize(version_base=None, config_path="configs"):
            config = compose(config_name="config")
            self._memory_analyzer = MemoryAnalyzer(config.batch_memory_percent)
            self._data_reader = DataReaderFactory.create(config.dataset, config.regime)

    @property
    def batch(self) -> DataBatch:
        """A data batch."""
        return self._batch

    def fill_batch_sequentially(self) -> None:
        """Adds elements with raw sensor measurements to the batch sequentially from the
        dataset.

        Raises:
            MemoryError: memory limit exceeded.
        """

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

        Raises:
            MemoryError: memory limit exceeded.
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

            MemoryError.
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
