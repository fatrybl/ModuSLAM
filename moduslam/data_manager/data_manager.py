import logging
from collections.abc import Sequence

from moduslam.data_manager.batch_factory.batch import Element
from moduslam.data_manager.batch_factory.factory import BatchFactory
from moduslam.logger.logging_config import data_manager
from moduslam.system_configs.data_manager.data_manager import DataManagerConfig
from moduslam.utils.auxiliary_dataclasses import PeriodicDataRequest

logger = logging.getLogger(data_manager)


class DataManager:
    """Manages all data processes."""

    def __init__(self, cfg: DataManagerConfig) -> None:
        """
        Args:
            cfg (DataManagerConfig): config for DataManager.
        """
        self._batch_factory = BatchFactory(cfg.batch_factory)
        logger.debug("Data Manager has been configured.")

    @property
    def batch_factory(self) -> BatchFactory:
        """Batch factory."""
        return self._batch_factory

    def make_batch_sequentially(self) -> None:
        """Creates a data batch sequentially based on regime."""
        self._batch_factory.batch.clear()
        self._batch_factory.fill_batch_sequentially()
        logger.debug("Data Batch has been created")

    def make_batch_by_elements(self, elements: Sequence[Element]) -> None:
        """Creates a data batch of elements with raw data.

        Args:
            elements: elements without raw data.
        """
        self._batch_factory.batch.clear()
        self._batch_factory.fill_batch_with_elements(elements)
        logger.debug("Data Batch has been created")

    def make_batch_by_requests(self, requests: Sequence[PeriodicDataRequest]) -> None:
        """Creates a data batch based on the requests.

        Args:
            requests: periodic data requests.
        """
        self._batch_factory.batch.clear()

        for request in requests:
            self._batch_factory.fill_batch_by_request(request)

        logger.debug("Data Batch has been created")
