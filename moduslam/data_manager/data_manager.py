import logging
from collections import deque
from typing import overload

from plum import dispatch

from moduslam.data_manager.factory.batch_factory import BatchFactory
from moduslam.data_manager.factory.element import Element
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
        self.batch_factory = BatchFactory(cfg.batch_factory)
        logger.debug("Data Manager has been configured.")

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
    def make_batch(self, requests: set[PeriodicDataRequest]) -> None:
        """
        @overload.

        Creates a data batch from requests.

        Args:
            requests (set[PeriodicDataRequest]): set of requests.

            Each request corresponds to sensor and time limits: (start, stop)
        """
        self.batch_factory.create_batch(requests)
        logger.debug("Data Batch has been created")

    @dispatch
    def make_batch(self, measurements=None):
        """
        @overload.

        Calls:
            1. Sequentially: create a batch with measurements sequentially.

            2. With measurements: create a batch with given measurements:
                Args:
                    measurements (deque[Element]): deque of elements without row data.

            3. With requests: create a batch with measurements from requests:
                Args:
                    requests (set[PeriodicDataRequest]): set of requests.

                    Each request corresponds to sensor and time limits: (start, stop).
        """
