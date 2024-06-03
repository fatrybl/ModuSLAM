from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from moduslam.data_manager.factory.element import Element
from moduslam.system_configs.frontend_manager.handlers.base_handler import HandlerConfig

if TYPE_CHECKING:
    from moduslam.frontend_manager.measurement_storage import Measurement


class Handler(ABC):
    """Base abstract handler for inheritance."""

    def __init__(self, config: HandlerConfig) -> None:
        """
        Args:
            config: configuration of the handler.
        """
        self._name = config.name

    @property
    def name(self) -> str:
        """Name of the handler."""
        return self._name

    @abstractmethod
    def process(self, element: Element) -> Measurement | None:
        """Processes the element.

        Args:
            element: element of data batch to be processed.

        Returns:
            measurement or None.
        """

    @abstractmethod
    def _create_empty_element(self, element: Element) -> Element:
        """Creates an empty element with the same timestamp, location and sensor as the
        input element. Must be used for creating elements for the measurement.

        Args:
            element: element of a data batch with raw data.

        Returns:
            empty element without data.
        """
