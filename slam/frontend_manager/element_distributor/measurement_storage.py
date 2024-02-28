import logging
from collections import deque
from dataclasses import dataclass
from typing import Any

from slam.data_manager.factory.element import Element
from slam.frontend_manager.handlers.ABC_handler import Handler
from slam.utils.auxiliary_dataclasses import TimeRange

logger = logging.getLogger(__name__)


@dataclass
class Measurement:
    """A measurement processed by a handler from element(s)."""

    time_range: TimeRange
    values: Any
    handler: Handler
    elements: tuple[Element, ...]


class MeasurementStorage:
    """Stores the measurements which have been processed by a handler."""

    def __init__(self) -> None:
        self.data: dict[Handler, deque[Measurement]] = {}
        self.recent_measurement: Measurement | None = None

    def add(self, handler: Handler, z: Measurement) -> None:
        """Adds a new measurement to the storage and updates last_timestamp attribute.

        Args:
            handler (Handler): external handler.
            z (Measurement): a new measurement to be added.
        """
        self.data[handler].append(z)
        self.recent_measurement = z
