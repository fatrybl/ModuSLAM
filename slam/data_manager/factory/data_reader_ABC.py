import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import overload

from plum import dispatch

from slam.data_manager.factory.element import Element
from slam.setup_manager.sensors_factory.sensors import Sensor
from slam.system_configs.system.data_manager.batch_factory.datasets.base_dataset import (
    DatasetConfig,
)
from slam.system_configs.system.data_manager.batch_factory.regime import (
    Stream,
    TimeLimit,
)

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
        """Base abstract class for any data reader.

        Args:
            regime (Stream | TimeLimit): data flow regime.
            dataset_params (DatasetConfig): data reader parameters.
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
            msg = f"File {file_path} does not exist."
            logger.error(msg)
            return False
        elif file_path.stat().st_size == 0:
            msg = f"File {file_path} is empty."
            logger.error(msg)
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
    def get_element(self, sensor: Sensor) -> Element | None:
        """
        @overload.
        Gets an element with raw sensor measurement from a dataset for
            a given sensor sequentially based on iterator position.

        Args:
            sensor (Sensor): a sensor to get measurement of.

        Returns:
            Element | None: element with raw sensor measurement
                or None if all measurements of the given sensor has already been processed.
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

        Raises:
            ItemNotFoundError: if the given element is not in the dataset.
        """

    @abstractmethod
    @overload
    def get_element(self, sensor: Sensor, timestamp: int) -> Element:
        """
        @overload.
        Gets an element with raw sensor measurement from a dataset
        for the given sensor and timestamp.

        Args:
            sensor (Sensor): a sensor to get measurement of.
            timestamp (int): timestamp of sensor`s measurement.

        Returns:
            (Element): with raw sensor measurement.

        Raises:
            ItemNotFoundError: if the given sensor`s measurement
                with the timestamp is not in the dataset.
        """

    @dispatch
    def get_element(self, element=None, timestamp=None):
        """
        @overload.

        Gets element from a dataset in different regimes based on arguments.

        Calls:
            1.
                Gets an element from a dataset sequentially based on iterator position.
                Args:
                    ___: None
                Returns:
                    Element | None: element with raw sensor measurement
                            or None if all measurements from a dataset has already been processed.
            2.
                Gets an element with raw sensor measurement from a dataset for
                                        a given sensor sequentially based on iterator position.
                Args:
                    sensor (Sensor): sensor to get measurement of.
                Returns:
                    Element | None: element with raw sensor measurement
                                    or None if any error.
            3.
                Gets an element with raw sensor measurement from a dataset for a given sensor and timestamp.
                Args:
                    sensor (Sensor): sensor to get measurement of.
                    timestamp (int | None): timestamp of sensor`s measurement.

                Returns:
                    element (Element): with raw sensor measurement.
                Raises:
                    ItemNotFoundError: if the given sensor`s measurement with the timestamp is not in the dataset.
            4.
                Gets an element with raw sensor`s measurement from a dataset for a given element
                w/o raw sensor measurement.
                Args:
                    element (Element): an element w/o raw sensor measurement.

                Returns:
                    element (Element): with raw sensor measurement.
                Raises:
                    ItemNotFoundError: if the given element is not in the dataset.

        """
