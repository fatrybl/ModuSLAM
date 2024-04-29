import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import overload

from plum import dispatch

from slam.data_manager.factory.element import Element
from slam.setup_manager.sensors_factory.sensors import Sensor
from slam.system_configs.data_manager.batch_factory.datasets.base_dataset import (
    DatasetConfig,
)
from slam.system_configs.data_manager.batch_factory.regime import Stream, TimeLimit

logger = logging.getLogger(__name__)


@dataclass
class DataFlowState(ABC):
    """Keeps up-to-date state of iterators for a data reader.

    Should be implemented for each reader.
    """


class DataReader(ABC):
    """Base abstract class for any data reader."""

    @abstractmethod
    def __init__(self, regime: Stream | TimeLimit, dataset_params: DatasetConfig) -> None:
        """
        Args:
            regime: data flow regime.
            dataset_params: parameters of the dataset.
        """

    @staticmethod
    def is_file_valid(file_path: Path) -> bool:
        """
        Checks if the file is valid: exists and not empty.

        Args:
            file_path: path to the file.
        """
        if not file_path.is_file():
            msg = f"File {file_path!r} does not exist."
            logger.critical(msg)
            return False
        elif file_path.stat().st_size == 0:
            msg = f"File {file_path!r} is empty."
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
            element with raw measurement or None if all measurements from a dataset has already been processed.
        """

    @abstractmethod
    @overload
    def get_element(self, sensor: Sensor) -> Element | None:
        """
        @overload.

        Gets element from a dataset sequentially based on iterator position for the specific sensor.

        Args:
            sensor: a sensor to get measurement of.

        Returns:
            element with raw measurement or None if all measurements from a dataset has already been processed.
        """

    @abstractmethod
    @overload
    def get_element(self, element: Element) -> Element:
        """
        @overload.

        Gets the element with raw measurement from a dataset for the given element without raw measurement.

        Args:
            element (Element): without raw measurement.

        Returns:
            element with raw measurement.

        Raises:
            ItemNotFoundError: the given element is not in the dataset.
        """

    @abstractmethod
    @overload
    def get_element(self, sensor: Sensor, timestamp: int) -> Element:
        """
        @overload.

        Gets an element with raw sensor measurement from a dataset for the given sensor and timestamp.

        Args:
            sensor (Sensor): a sensor to get measurement of.

            timestamp (int): timestamp of sensor`s measurement.

        Returns:
            element with raw measurement.

        Raises:
            ItemNotFoundError: the element of the given sensor and timestamp is not in the dataset.
        """

    @dispatch
    def get_element(self, element=None, timestamp=None):
        """
        @overload.

        Gets element from a dataset in different regimes based on arguments.

        Calls:
            1.  Gets element from a dataset sequentially based on iterator position for the specific sensor.

                Args:
                    __.

                Returns:
                    element (Element) with raw measurement or None if all measurements from a dataset has already been processed.

            2.  Gets the element with raw measurement from a dataset for the given element without raw measurement.

                Args:
                    sensor (Sensor): sensor to get measurement of.

                Returns:
                    element (Element) with raw measurement.

            3.  Gets the element with raw measurement from a dataset for the given element without raw measurement.

                Args:
                    element (Element): without raw measurement.

                Returns:
                    element with raw measurement.

                Raises:
                    ItemNotFoundError: the given element is not in the dataset.

            4.  Gets an element with raw sensor measurement from a dataset for the given sensor and timestamp.

                Args:
                    sensor (Sensor): sensor to get measurement of.

                    timestamp (int): timestamp of sensor`s measurement.

                Returns:
                    element (Element) with raw measurement.

                Raises:
                    ItemNotFoundError: the element of the given sensor and timestamp is not in the dataset.
        """
