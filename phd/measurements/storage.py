import logging

from phd.logger.logging_config import frontend_manager
from phd.measurements.processed import Measurement
from phd.measurements.time_updater import TimeRangeUpdate
from phd.moduslam.utils.auxiliary_dataclasses import TimeRange
from phd.moduslam.utils.exceptions import (
    EmptyStorageError,
    ItemExistsError,
    ItemNotExistsError,
    ValidationError,
)
from phd.moduslam.utils.ordered_set import OrderedSet

logger = logging.getLogger(frontend_manager)


class MeasurementStorage:
    """Storage for measurements."""

    def __init__(self) -> None:
        self._data: dict[type[Measurement], OrderedSet[Measurement]] = {}
        self._start_timestamp: int | None = None
        self._stop_timestamp: int | None = None
        self._recent_measurement: Measurement | None = None

    def __contains__(self, item) -> bool:
        t_item = type(item)
        return t_item in self._data and item in self._data[t_item]

    @property
    def data(self) -> dict[type[Measurement], OrderedSet[Measurement]]:
        """Dictionary with typed OrderedSets."""
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
            logger.error(msg)
            raise EmptyStorageError(msg)

    @property
    def time_range(self) -> TimeRange:
        """Start & stop time margins to cover all measurements in the storage.

        Raises:
            EmptyStorageError: time range does not exist for empty storage.
        """
        if self._start_timestamp is not None and self._stop_timestamp is not None:
            return TimeRange(self._start_timestamp, self._stop_timestamp)

        else:
            msg = "Time range does not exist for empty storage."
            logger.error(msg)
            raise EmptyStorageError(msg)

    @property
    def empty(self) -> bool:
        """Checks if the storage is empty."""
        return not bool(self._data)

    def add(self, measurement: Measurement) -> None:
        """Adds new measurement to the storage.

        Args:
            measurement: a measurement to add.

        Raises:
            ValidationError: if measurement is already present in the storage.
        """
        try:
            self._validate_new_measurement(measurement)
        except ItemExistsError as e:
            logger.error(e)
            raise ValidationError(e)

        m_type = type(measurement)
        self._data.setdefault(m_type, OrderedSet()).add(measurement)

        self._start_timestamp, self._stop_timestamp = TimeRangeUpdate.update_time_range_on_add(
            measurement, self._start_timestamp, self._stop_timestamp
        )
        self._update_recent_measurement(measurement)

    def remove(self, measurement: Measurement) -> None:
        """Removes the measurement from the storage.

        Args:
            measurement: the measurement to remove.

        Raises:
            ValidationError: if measurement is not present in the storage.
        """
        try:
            self._validate_removing_measurement(measurement)
        except ItemNotExistsError as e:
            logger.error(e)
            raise ValidationError(e)

        m_type = type(measurement)
        self._data[m_type].remove(measurement)

        if not self._data[m_type]:
            del self._data[m_type]

        if measurement == self._recent_measurement:
            self._recent_measurement = self._find_recent_measurement()

        self._start_timestamp, self._stop_timestamp = TimeRangeUpdate.update_time_range_on_removal(
            self._data, measurement, self._start_timestamp, self._stop_timestamp
        )

    def clear(self) -> None:
        """Clears the storage."""
        self._start_timestamp = None
        self._stop_timestamp = None
        self._data.clear()

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

    def _validate_new_measurement(self, measurement: Measurement) -> None:
        """Validates a new measurement before adding.

        Args:
            measurement: a measurement to be added.

        Raises:
            ItemExistsError: if a measurement is already present in the storage.
        """
        m_type = type(measurement)

        if m_type in self._data and measurement in self._data[m_type]:
            raise ItemExistsError(f"Measurement {measurement} already exists in the storage.")

    def _validate_removing_measurement(self, measurement: Measurement) -> None:
        """Validates a measurement before removing.

        Args:
            measurement: a measurement to be removed.

        Raises:
            ItemNotExistsError: if a measurement is not present in the storage.
        """
        m_type = type(measurement)

        if m_type not in self._data or measurement not in self._data[m_type]:
            raise ItemNotExistsError(f"Measurement {measurement} does not exist in the storage.")
