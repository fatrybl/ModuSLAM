import logging
from abc import ABC, abstractmethod
from types import TracebackType
from typing import overload

from plum import dispatch

from phd.logger.logging_config import data_manager
from phd.moduslam.data_manager.batch_factory.batch import Element
from phd.moduslam.data_manager.batch_factory.configs import DatasetConfig
from phd.moduslam.data_manager.batch_factory.regimes import Stream, TimeLimit
from phd.moduslam.sensors_factory.sensors import Sensor

logger = logging.getLogger(data_manager)


class DataReaderState(ABC):
    """Stores positions of iterators for sequential data reading."""


class DataReader(ABC):
    """Base abstract class for any data reader."""

    _context_error_msg: str = "Method must be called within a context."

    def __init__(self, regime: Stream | TimeLimit, dataset_params: DatasetConfig) -> None:
        """
        Args:
            regime: data flow regime.

            dataset_params: parameters of the dataset.
        """
        self._regime = regime
        self._dataset_params = dataset_params
        self._in_context: bool = False

    @abstractmethod
    def __enter__(self):
        """Opens the dataset for reading."""

    @abstractmethod
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ):
        """Closes the dataset after reading."""

    @abstractmethod
    def set_initial_state(self, sensor: Sensor, timestamp: int) -> None:
        """Sets the iterator(s) position(s) for the given sensor and timestamp.

        Args:
            sensor: sensor to set the iterator(s) position(s) to.

            timestamp: timestamp to set the iterator(s) position(s) to.

        Raises:
            SetNotStateError: if no measurement for the given sensor and timestamp has been found.
        """

    @abstractmethod
    @overload
    def get_next_element(self) -> Element | None:
        """
        @overload.

        Gets element from a dataset sequentially based on iterator position.

        Returns:
            element with raw measurement or None if all measurements from a dataset have already been read.

        Raises:
            RuntimeError: if the method is called outside the context manager.
        """

    @abstractmethod
    @overload
    def get_next_element(self, sensor: Sensor) -> Element | None:
        """
        @overload.

        Gets element from a dataset sequentially based on iterator position for the specific sensor.

        Args:
            sensor: a sensor to get measurement of.

        Returns:
            element with raw measurement or None if all measurements from a dataset has already been processed.

        Raises:
            RuntimeError: if the method is called outside the context manager.
        """

    @dispatch
    def get_next_element(self, sensor=None):
        """
        @overload.

        Gets element from a dataset in different regimes based on arguments.

        Calls:
            1.  Gets element from a dataset sequentially based on iterator position for the specific sensor.

                Args:
                    __.

                Returns:
                    element (Element) with raw measurement or None if all measurements from a dataset
                    has already been processed.

                Raises:
                    RuntimeError: if the method is called outside the context manager.

            2.  Gets element from a dataset sequentially based on iterator position for the specific sensor.

                Args:
                    sensor (Sensor): sensor to get the next measurement of.

                Returns:
                    element (Element) with raw measurement or None
                    if all measurements for the given sensor have already been processed.

                Raises:
                    RuntimeError: if the method is called outside the context manager.
        """

    @abstractmethod
    def get_element(self, element: Element) -> Element:
        """Gets the element with raw measurement from a dataset for the given element
        without raw measurement.

        Args:
            element: existing element without raw measurement.

        Returns:
            element with raw measurement.

        Raises:
            RuntimeError: if the method is called outside the context manager.
        """
