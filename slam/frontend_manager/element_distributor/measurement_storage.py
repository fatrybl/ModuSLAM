import logging
from dataclasses import dataclass
from typing import Any, overload

from plum import dispatch

from slam.data_manager.factory.element import Element
from slam.frontend_manager.handlers.ABC_handler import Handler
from slam.utils.auxiliary_dataclasses import TimeRange
from slam.utils.ordered_set import OrderedSet

logger = logging.getLogger(__name__)


@dataclass(frozen=True, eq=True)
class Measurement:
    """A measurement formed of processed element(s) by the corresponding handler.

    Hash calculation ignores "values" field because not all values are hashable.
    """

    time_range: TimeRange
    values: Any
    handler: Handler
    elements: tuple[Element, ...]

    def __hash__(self):
        return hash((self.time_range, self.handler, self.elements))


class MeasurementStorage:
    """Stores the measurements which have been processed by handlers."""

    def __init__(self) -> None:
        self._data: dict[Handler, OrderedSet[Measurement]] = {}

    @property
    def data(self) -> dict[Handler, OrderedSet[Measurement]]:
        """Dictionary with "handler -> measurements" data."""
        return self._data

    @property
    def recent_measurement(self) -> Measurement:
        """A measurement with latest "stop" timestamp in the storage."""
        try:
            __, measurement = self._update_state()
            return measurement
        except AssertionError:
            raise IndexError("Empty storage: recent measurement does not exist.")

    @property
    def time_range(self) -> TimeRange:
        """Time range of the storage."""
        try:
            time_range, __ = self._update_state()
            return time_range
        except AssertionError:
            raise IndexError("Empty storage: time range does not exist.")

    @property
    def is_empty(self) -> bool:
        """Checks if the storage is empty."""
        return not bool(self._data)

    @overload
    def add(self, measurement: Measurement) -> None:
        """Adds a new measurement to the storage.

        Args:
            measurement (Measurement): a new measurement to be added.
        """

        if measurement.handler in self._data:
            self._data[measurement.handler].add(measurement)
        else:
            self._data.update({measurement.handler: OrderedSet([measurement])})

    @overload
    def add(self, data: dict[Handler, OrderedSet[Measurement]]) -> None:
        """Adds a new "handler -> measurements" dict to the storage.

        Attention: might be slow due to the "recent_measurement" update.
        Args:
            data (dict[Handler, OrderedSet[Measurement]]): dict to add.
        """
        self._data = self._data | data

    @dispatch
    def add(self, measurement=None):
        """
        @overload.
        Args:
            measurement (Measurement): a new measurement to be added.
        """

    def remove(self, measurement: Measurement) -> None:
        """Removes the measurement from the storage."""
        self._data[measurement.handler].remove(measurement)
        if not self._data[measurement.handler]:
            del self._data[measurement.handler]

    def clear(self) -> None:
        """Clears the storage."""
        self._data.clear()

    def _update_state(self) -> tuple[TimeRange, Measurement]:
        """Updates the time range of the storage.

        TODO: the time range might be updated quicker then O(N).
        """
        assert self._data, "Empty storage: no measurements."

        measurements: OrderedSet[Measurement] = OrderedSet()
        for ord_set in self._data.values():
            [measurements.add(m) for m in ord_set]

        m_start = min(measurements, key=lambda m: m.time_range.start)
        m_stop = max(measurements, key=lambda m: m.time_range.stop)

        time_range = TimeRange(m_start.time_range.start, m_stop.time_range.stop)
        recent_measurement = m_stop

        del measurements

        return time_range, recent_measurement
