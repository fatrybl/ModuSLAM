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

    Hash calculation ignores "values" attribute because not all values are hashable.
    """

    time_range: TimeRange
    values: Any
    handler: Handler
    elements: tuple[Element, ...]
    noise_covariance: tuple[float, ...]

    def __hash__(self):
        return hash(
            (
                self.time_range,
                self.handler,
                self.elements,
                self.noise_covariance,
            )
        )


class MeasurementStorage:
    """Storage for measurements."""

    def __init__(self) -> None:
        self._data: dict[Handler, OrderedSet[Measurement]] = {}

    @property
    def data(self) -> dict[Handler, OrderedSet[Measurement]]:
        """Dictionary with "handler -> measurements" pairs."""
        return self._data

    @property
    def recent_measurement(self) -> Measurement:
        """A measurement with latest "stop" timestamp in the storage.

        Raises:
            IndexError: if the storage is empty.
        """
        try:
            __, measurement = self._update_state()
            return measurement
        except AssertionError:
            raise IndexError("Empty storage: recent measurement does not exist.")

    @property
    def time_range(self) -> TimeRange:
        """Start & stop time margins to cover all measurements in the storage.

        Raises:
            IndexError: time range does not exists for empty storage.
        """
        try:
            time_range, __ = self._update_state()
            return time_range
        except AssertionError:
            raise IndexError("Empty storage: time range does not exist.")

    @property
    def empty(self) -> bool:
        """Checks if the storage is empty."""
        return not bool(self._data)

    @overload
    def add(self, measurement: Measurement) -> None:
        """Adds new measurement to the storage.

        Args:
            measurement: the measurement to add.
        """

        if measurement.handler in self._data:
            self._data[measurement.handler].add(measurement)
        else:
            self._data.update({measurement.handler: OrderedSet([measurement])})

    @overload
    def add(self, data: dict[Handler, OrderedSet[Measurement]]) -> None:
        """
        @overload.

        Adds multiple measurements to the storage in "handler -> measurements" table format.

        Attention:
            might be slow due to the "recent_measurement" update.

        Args:
            data: measurements to add.
        """
        self._data = self._data | data

    @dispatch
    def add(self, measurement=None):
        """
        @overload.

        Adds measurement(s) to the storage.

        Calls:
            1. Adds new measurement to the storage.

                Args:
                    measurement (Measurement): the measurement to add.

            2.  Adds multiple measurements to the storage in "handler -> measurements" table format.

                Args:
                    data (dict[Handler, OrderedSet[Measurement]]): measurements to add.

                Attention:
                    might be slow due to the "recent_measurement" update.

        """

    def remove(self, measurement: Measurement) -> None:
        """Removes the measurement from the storage.

        Args:
            measurement: the measurement to remove.
        """
        self._data[measurement.handler].remove(measurement)
        if not self._data[measurement.handler]:
            del self._data[measurement.handler]

    def clear(self) -> None:
        """Clears the storage."""
        self._data.clear()

    def _update_state(self) -> tuple[TimeRange, Measurement]:
        """Updates the time range of the storage.

        TODO: the time range might be updated quicker then O(N).

        Returns:
            time range, recent measurement with latest "stop" timestamp.
        """
        assert self._data, "Empty storage: no measurements."

        measurements = OrderedSet[Measurement]()
        for ordered_set in self._data.values():
            measurements.add(ordered_set)

        m_start = min(measurements, key=lambda m: m.time_range.start)
        m_stop = max(measurements, key=lambda m: m.time_range.stop)

        time_range = TimeRange(m_start.time_range.start, m_stop.time_range.stop)
        recent_measurement = m_stop

        del measurements

        return time_range, recent_measurement
