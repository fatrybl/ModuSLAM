import logging

from plum import dispatch

from configs.system.data_manager.data_manager import DataManagerConfig
from slam.data_manager.factory.batch_factory import BatchFactory
from slam.data_manager.factory.readers.element_factory import Element
from slam.utils.auxiliary_dataclasses import PeriodicData
from slam.utils.meta_singleton import MetaSingleton

logger = logging.getLogger(__name__)


class DataManager(metaclass=MetaSingleton):
    """Manages all data processes. Defaults to MetaSingleton."""

    def __init__(self, cfg: DataManagerConfig) -> None:
        """
        Args:
            cfg (DataManagerConfig): config for DataManager.
        """
        self.batch_factory = BatchFactory(cfg.batch_factory)
        logger.debug("Data Manager has been configured")

    @dispatch
    def make_batch(self) -> None:
        """
        Creates a data batch sequentially based on regime in config.
        """
        self.batch_factory.create_batch()
        logger.debug("Data Batch has been created")

    @dispatch
    def make_batch(self, measurements: list[Element]) -> None:
        """
        Creates a data batch with given measurements

        Args:
            measurements (list[Element]): list of elements wihtout row data
        """
        self.batch_factory.create_batch(measurements)
        logger.debug("Data Batch has been created")

    @dispatch
    def make_batch(self, requests: set[PeriodicData]) -> None:
        """Creates a data batch from requests.

        Args:
            requests (set[PeriodicData]): set of requests.
            Each request corresponds to sensor and time limits: (start, stop)
        """
        self.batch_factory.create_batch(requests)
        logger.debug("Data Batch has been created")
