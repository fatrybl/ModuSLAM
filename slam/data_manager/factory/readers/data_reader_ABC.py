import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import overload

from plum import dispatch

from configs.system.data_manager.batch_factory.datasets.base_dataset import (
    DatasetConfig,
)
from configs.system.data_manager.batch_factory.regime import RegimeConfig
from slam.data_manager.factory.readers.element_factory import Element
from slam.setup_manager.sensor_factory.sensors import Sensor

logger = logging.getLogger(__name__)


@dataclass
class DataFlowState(ABC):
    """Keeps up-to-date state of iterators for a data reader.
    Should be implemented for each reader."""


class DataReader(ABC):
    """Base abstract class for any data reader."""

    def __init__(self, dataset_params: DatasetConfig, regime_params: RegimeConfig) -> None:
        """
        Base abstract class for any data reader.
        Args:
            dataset_params (DatasetConfig): parameters of the data reader.
            regime_params (RegimeConfig): data reader regime parameters.
        """

    @staticmethod
    def is_file_valid(file_path: Path) -> bool:
        """
        Checks if a file is valid: exists and not empty.
        Args:
            file_path (Path): path to a file.

        Returns:
            bool: True if file is valid, False otherwise.
        """
        if not Path.is_file(file_path):
            msg = f"File {file_path} does not exist"
            logger.critical(msg)
            return False
        elif file_path.stat().st_size == 0:
            msg = f"File {file_path} is empty"
            logger.critical(msg)
            return False
        else:
            return True

    @abstractmethod
    @overload
    def get_element(self) -> Element | None:
        """
        @overload.
        Gets element from a dataset sequentially based on iterator position.

        Returns:
            Element | None: element with raw sensor measurement
                            or None if all measurements from a dataset has already been processed
        """

    @abstractmethod
    @overload
    def get_element(self, element: Element) -> Element:
        """
        @overload.
        Gets an element with raw sensor measurement from a dataset for
            a given element without raw sensor measurement.

        Args:
            element (Element): without raw sensor measurement.

        Returns:
            (Element): with raw sensor measurement.
        """

    @abstractmethod
    @overload
    def get_element(self, sensor: Sensor, timestamp: int | None = None) -> Element:
        """
        @overload.
        Gets an element with raw sensor measurement from a dataset for
            a given sensor and timestamp. If timestamp is None,
            gets the element sequantally based on iterator position.

        Args:
            sensor (Sensor): a sensor to get measurement of.
            timestamp (int | None, optional): timestamp of sensor`s measurement. Defaults to None.

        Returns:
            (Element): with raw sensor measurement.
        """

    @dispatch
    def get_element(self, element=None, timestamp=None):
        """
        @overload.
        """
