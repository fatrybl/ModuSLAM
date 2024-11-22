import logging
from collections.abc import Iterable

from phd.logger.logging_config import frontend_manager
from phd.measurements.processed_measurements import Measurement
from phd.measurements.time_updater import TimeRangeUpdate
from phd.moduslam.utils.auxiliary_dataclasses import TimeRange
from phd.moduslam.utils.exceptions import EmptyStorageError
from phd.moduslam.utils.ordered_set import OrderedSet

logger = logging.getLogger(frontend_manager)


class MeasurementStorage:
    """Storage for measurements."""

    def __init__(self) -> None:
        self._data: dict[type[Measurement], OrderedSet[Measurement]] = {}
        self._start_timestamp: int | None = None
        self._stop_timestamp: int | None = None
        self._recent_measurement: Measurement | None = None

    @property
    def data(self) -> dict[type[Measurement], OrderedSet[Measurement]]:
        """Dictionary with "handler -> measurements" pairs."""
        return self._data

    @property
    def recent_measurement(self) -> Measurement:
        """A measurement with the latest "stop" timestamp in the storage.

        Raises:
            EmptyStorageError: recent measurement does not exist in empty storage.
        """
        if self._recent_measurement:
            return self._recent_measurement
        else:
            msg = "Recent measurement does not exist in empty storage."
            logger.debug(msg)
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
        self._start_timestamp = None
        self._stop_timestamp = None
        self._data.clear()

    def _add(self, measurement: Measurement) -> None:
        """Adds new measurement to the storage.

        Args:
            measurement: a measurement to add.
        """
        m_type = type(measurement)
        self._data.setdefault(m_type, OrderedSet()).add(measurement)

        self._start_timestamp, self._stop_timestamp = TimeRangeUpdate.update_time_range_on_add(
            measurement, self._start_timestamp, self._stop_timestamp
        )
        self._update_recent_measurement(measurement)

    def _remove(self, measurement: Measurement) -> None:
        """Removes the measurement from the storage.

        Args:
            measurement: the measurement to remove.
        """
        m_type = type(measurement)

        if m_type in self._data:
            if measurement in self._data[m_type]:
                self._data[m_type].remove(measurement)

        if not self._data[m_type]:
            del self._data[m_type]

        if measurement == self._recent_measurement:
            self._recent_measurement = self._find_recent_measurement()

        TimeRangeUpdate.update_time_range_on_removal(
            self._data, measurement, self._start_timestamp, self._stop_timestamp
        )

    def _update_recent_measurement(self, measurement: Measurement) -> None:
        """Updates the recent measurement in the storage by comparing the "stop"
        timestamp of measurement`s time range.

        Args:
            measurement: new measurement to compare with.
        """
        if (
            self._recent_measurement is None
            or measurement.timestamp > self._recent_measurement.timestamp
        ):
            self._recent_measurement = measurement

    def _find_recent_measurement(self) -> Measurement | None:
        """Finds the measurement with the latest "stop" timestamp in the storage."""
        if not self._data:
            return None

        recent_measurement = max(
            (measurement for measurements in self._data.values() for measurement in measurements),
            key=lambda measurement: measurement.timestamp,
            default=None,
        )
        return recent_measurement
