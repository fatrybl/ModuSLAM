from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Type
import logging

from pathlib import Path

from plum import dispatch

from slam.data_manager.factory.readers.element_factory import Element
from slam.setup_manager.sensor_factory.sensors import Sensor

logger = logging.getLogger(__name__)


class DataReader(ABC):
    """Base abstract class for any data reader."""

    @staticmethod
    def is_file_valid(file_path: Path) -> bool:
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
    @dispatch
    def get_element(self) -> Element | None:
        """
        Gets element from a dataset sequantially based on iterator position. 

        Returns:
            Element | None: element with raw sensor measurement 
                            or None if all measurements from a dataset has already been processed
        """

    @abstractmethod
    @dispatch
    def get_element(self, element: Element) -> Element:
        """
        Gets an element with raw sensor measurement from a dataset for 
            a given element without raw sensor measurement.

        Args:
            element (Element): without raw sensor measurement.

        Returns:
            Element: with raw sensor measurement.
        """

    @abstractmethod
    @dispatch
    def get_element(self, sensor: Sensor, timestamp: int | None = None) -> Element:
        """
        Gets an element with raw sensor measurement from a dataset for 
            a given sensor and timestamp. If timestamp is None, 
            gets the element sequantally based on iterator position.

        Args:
            sensor (Sensor): a sensor to get measurement of.
            timestamp (int | None, optional): timestamp of sensor`s measurement. Defaults to None.

        Returns:
            Element: with raw sensor measurement.
        """


@dataclass
class DataFlowState(ABC):
    """Keeps up-to-date state of iterators for a data reader. 
    Should be implemented for each reader."""
