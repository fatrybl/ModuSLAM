import logging
from collections import deque
from dataclasses import dataclass
from typing import Any

from slam.data_manager.factory.readers.element_factory import Element
from slam.frontend_manager.handlers.ABC_handler import Handler
from slam.utils.auxiliary_dataclasses import TimeRange

logger = logging.getLogger(__name__)


@dataclass
class Measurement:
    """
    A measurement processed by a handler from element(s).
    """

    time_range: TimeRange
    values: Any
    handler: Handler
    elements: tuple[Element, ...]


class MeasurementStorage:
    """
    Stores the measurements which have been processed by a handler.
    """

    def __init__(self) -> None:
        self.data: dict[Handler, deque[Measurement]] = {}
        self._last_timestamp: int | None = None

    @property
    def last_timestamp(self) -> int:
        """
        The timestamp of the last added measurement.
        Returns:
            (int): timestamp of the last added measurement.
        Raises:
            ValueError: if the timestamp is None.
        """
        if self._last_timestamp is not None:
            return self._last_timestamp
        else:
            msg = "The last measurement timestamp is None."
            logger.error(msg)
            raise ValueError

    def add(self, handler: Handler, z: Measurement) -> None:
        """
        Adds a new measurement to the storage and updates last_timestamp attribute.
        Args:
            handler (Handler): external handler.
            z (Measurement): a new measurement to be added.

        """
        self.data[handler].append(z)
