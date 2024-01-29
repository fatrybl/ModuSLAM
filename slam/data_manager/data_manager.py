import logging
from collections import deque
from typing import overload

from plum import dispatch

from configs.system.data_manager.data_manager import DataManagerConfig
from slam.data_manager.factory.batch_factory import BatchFactory
from slam.data_manager.factory.readers.element_factory import Element
from slam.utils.auxiliary_dataclasses import PeriodicData

logger = logging.getLogger(__name__)


class DataManager:
    """Manages all data processes. Defaults to MetaSingleton."""

    def __init__(self, cfg: DataManagerConfig) -> None:
        """
        Args:
            cfg (DataManagerConfig): config for DataManager.
        """
        self.batch_factory = BatchFactory(cfg.batch_factory)
        logger.debug("Data Manager has been configured")

    @overload
    def make_batch(self) -> None:
        """
        @overload.
        Creates a data batch sequentially based on regime in config.
        """
        self.batch_factory.create_batch()
        logger.debug("Data Batch has been created")

    @overload
    def make_batch(self, measurements: deque[Element]) -> None:
        """
        @overload.
        Creates a data batch with given measurements

        Args:
            measurements (deque[Element]): list of elements without row data
        """
        self.batch_factory.create_batch(measurements)
        logger.debug("Data Batch has been created")

    @overload
    def make_batch(self, requests: set[PeriodicData]) -> None:
        """
        @overload.
        Creates a data batch from requests.

        Args:
            requests (set[PeriodicData]): set of requests.
            Each request corresponds to sensor and time limits: (start, stop)
        """
        self.batch_factory.create_batch(requests)
        logger.debug("Data Batch has been created")

    @dispatch
    def make_batch(self, measurements=None):
        """
        @overload.

        Calls:
            1. Sequentially: create a batch with measurements sequentially:
                Args:
                    None

            2. With measurements: create a batch with given measurements:
                Args:
                    measurements (deque[Element]): deque of elements without row data.

            3. With requests: create a batch with measurements from requests:
                Args:
                    requests (set[PeriodicData]): set of requests.
                    Each request corresponds to sensor and time limits: (start, stop).
        """
