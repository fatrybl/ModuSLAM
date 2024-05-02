import logging
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

from slam.data_manager.factory.element import Element
from slam.frontend_manager.handlers.ABC_handler import Handler
from slam.logger.logging_config import frontend_manager_logger
from slam.utils.auxiliary_dataclasses import TimeRange
from slam.utils.exceptions import EmptyStorageError
from slam.utils.ordered_set import OrderedSet

logger = logging.getLogger(frontend_manager_logger)


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

        self._start_timestamp: int | None = None
        self._stop_timestamp: int | None = None

        self._recent_measurement: Measurement | None = None

    @property
    def data(self) -> dict[Handler, OrderedSet[Measurement]]:
        """Dictionary with "handler -> measurements" pairs."""
        return self._data

    @property
    def recent_measurement(self) -> Measurement:
        """A measurement with latest "stop" timestamp in the storage.

        Raises:
            EmptyStorageError: recent measurement does not exist in empty storage.
        """
        if self._recent_measurement:
            return self._recent_measurement
        else:
            msg = "Recent measurement does not exist in empty storage."
            logger.critical(msg)
            raise EmptyStorageError(msg)

    @property
    def time_range(self) -> TimeRange:
        """Start & stop time margins to cover all measurements in the storage.

        Raises:
            IndexError: time range does not exist for empty storage.
        """
        if self._start_timestamp is not None and self._stop_timestamp is not None:
            return TimeRange(self._start_timestamp, self._stop_timestamp)

        else:
            msg = "Time range does not exist for empty storage."
            logger.critical(msg)
            raise EmptyStorageError(msg)

    @property
    def empty(self) -> bool:
        """Checks if the storage is empty."""
        return not bool(self._data)

    def add(self, measurement: Measurement | Iterable[Measurement]) -> None:
        """Adds measurement(s) to the storage.

        Args:
            measurement: measurement(s) to add.
        """
        if isinstance(measurement, Iterable):
            for m in measurement:
                self._add(m)
        else:
            self._add(measurement)

    def remove(self, measurement: Measurement | Iterable[Measurement]) -> None:
        """Removes the measurement(s) from the storage.

        Args:
            measurement: the measurement(s) to be removed.
        """
        if isinstance(measurement, Iterable):
            for m in measurement:
                self._remove(m)
        else:
            self._remove(measurement)

    def clear(self) -> None:
        """Clears the storage."""
        self._data.clear()

    def _add(self, measurement: Measurement) -> None:
        """Adds new measurement(s) to the storage.

        Args:
            measurement: the measurement to add.
        """

        if measurement.handler in self._data:
            self._data[measurement.handler].add(measurement)
        else:
            self._data.update({measurement.handler: OrderedSet([measurement])})

        self._update_time_range(measurement.time_range)
        self._update_recent_measurement(measurement)

    def _remove(self, measurement: Measurement) -> None:
        """Removes the measurement from the storage.

        Args:
            measurement: the measurement to remove.
        """
        self._data[measurement.handler].remove(measurement)
        if not self._data[measurement.handler]:
            del self._data[measurement.handler]

    def _update_recent_measurement(self, measurement: Measurement) -> None:
        """Updates the recent measurement in the storage by comparing the "stop"
        timestamp of measurement`s time range.

        Args:
            measurement: new measurement to compare with.
        """
        if (
            self._recent_measurement is None
            or measurement.time_range.stop > self._recent_measurement.time_range.stop
        ):
            self._recent_measurement = measurement

    def _update_time_range(self, time_range: TimeRange) -> None:
        """Updates the time range of the storage.

        Args:
            time_range: time range to update.
        """

        if self._start_timestamp is None or time_range.start < self._start_timestamp:
            self._start_timestamp = time_range.start
        if self._stop_timestamp is None or time_range.stop > self._stop_timestamp:
            self._stop_timestamp = time_range.stop
