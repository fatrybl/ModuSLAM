import logging
from collections.abc import Iterable
from types import TracebackType
from typing import Any, Protocol, overload, runtime_checkable

from plum import dispatch

from src.moduslam.data_manager.batch_factory.batch import Element
from src.moduslam.data_manager.batch_factory.regimes import Stream, TimeLimit
from src.moduslam.sensors_factory.sensors import Sensor

logger = logging.getLogger("data_manager")

context_error_msg: str = "Method must be called within a context."
configuration_error_msg: str = "Reader has not been configured. Call the configure() method first."


@runtime_checkable
class DataReader(Protocol):
    """Interface for any data reader."""

    def __enter__(self) -> "DataReader":
        """Opens the dataset for reading."""

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Closes the dataset after reading."""

    def configure(
        self, regime: Stream | TimeLimit, sensors: Iterable[Sensor], *args: Any, **kwargs: Any
    ) -> None:
        """Configures the Reader for get_next_element() overloads.

        Args:
            regime: data collection regime.

            sensors: sensors to read data of.

            *args: additional arguments.

            **kwargs: additional keyword arguments.
        """

    def set_initial_state(self, sensor: Sensor, timestamp: int) -> None:
        """ "Performs the necessary setup for the required configuration or initialization."

        TODO: method is not required for all readers. Maybe remove it from BatchFactory ?
        Args:
            sensor: a sensor to set up.

            timestamp: a timestamp to set up.

        Raises:
            SetNotStateError: if no measurement has been found for the given sensor and timestamp.
        """

    @overload
    def get_next_element(self) -> Element | None:
        """
        Gets element from a dataset sequentially based on iterator position.

        Returns:
            element with raw measurement or None if all measurements from a dataset have already been read.

        Raises:
            RuntimeError: if a method has been called outside the context manager.
        """

    @overload
    def get_next_element(self, sensor: Sensor) -> Element | None:
        """
        Gets element from a dataset sequentially based on iterator position for the specific sensor.

        Args:
            sensor: a sensor to get measurement of.

        Returns:
            element with raw measurement or None if all measurements from a dataset has already been processed.

        Raises:
            RuntimeError: if a method has been called outside the context manager.
        """

    @dispatch
    def get_next_element(self, sensor: Sensor | None = None) -> Element | None:
        """
        Gets element from a dataset in different regimes based on arguments.
        """

    def get_element(self, element: Element) -> Element:
        """Gets the element with raw measurement from a dataset for the given element
        without raw measurement.

        Args:
            element: existing element without raw measurement.

        Returns:
            element with raw measurement.

        Raises:
            ItemNotFoundError: if no real measurement has been found
            in the dataset for the given element.
        """
