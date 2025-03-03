import logging

from src.logger.logging_config import frontend_manager
from src.measurement_storage.measurements.base import Measurement
from src.measurement_storage.measurements.time_limits_updater import Updater
from src.utils.auxiliary_dataclasses import TimeRange
from src.utils.exceptions import (
    EmptyStorageError,
    ItemExistsError,
    ItemNotExistsError,
    ValidationError,
)
from src.utils.ordered_set import OrderedSet

logger = logging.getLogger(frontend_manager)


class MeasurementStorage:
    """Global Storage for the processed measurements."""

    _data: dict[type[Measurement], OrderedSet[Measurement]] = {}
    _start_timestamp: int | None = None
    _stop_timestamp: int | None = None
    _recent_measurement: Measurement | None = None

    @classmethod
    def data(cls) -> dict[type[Measurement], OrderedSet[Measurement]]:
        """Dictionary with typed OrderedSets."""
        return cls._data

    @classmethod
    def recent_measurement(cls) -> Measurement:
        """A measurement with the latest "stop" timestamp in the storage.

        Raises:
            EmptyStorageError: recent measurement does not exist in empty storage.
        """
        if cls._recent_measurement:
            return cls._recent_measurement
        else:
            msg = "Recent measurement does not exist in empty storage."
            logger.error(msg)
            raise EmptyStorageError(msg)

    @classmethod
    def time_range(cls) -> TimeRange:
        """Start & stop time margins to cover all measurements in the storage.

        Raises:
            EmptyStorageError: time range does not exist for empty storage.
        """
        if cls._start_timestamp is not None and cls._stop_timestamp is not None:
            return TimeRange(cls._start_timestamp, cls._stop_timestamp)

        else:
            msg = "Time range does not exist for empty storage."
            logger.error(msg)
            raise EmptyStorageError(msg)

    @classmethod
    def empty(cls) -> bool:
        """Checks if the storage is empty."""
        return not bool(cls._data)

    @classmethod
    def add(cls, measurement: Measurement) -> None:
        """Adds new measurement to the storage.

        Args:
            measurement: a measurement to add.

        Raises:
            ValidationError: if measurement is already present in the storage.
        """
        try:
            cls._validate_new_measurement(measurement)
        except ItemExistsError as e:
            logger.error(e)
            raise ValidationError(e)

        m_type = type(measurement)
        cls._data.setdefault(m_type, OrderedSet()).add(measurement)

        cls._start_timestamp, cls._stop_timestamp = Updater.update_start_stop_on_adding(
            measurement, cls._start_timestamp, cls._stop_timestamp
        )
        cls._update_recent_measurement(measurement)

    @classmethod
    def remove(cls, measurement: Measurement) -> None:
        """Removes the measurement from the storage.

        Args:
            measurement: the measurement to remove.

        Raises:
            ValidationError: if measurement is not present in the storage.
        """
        try:
            cls._validate_removing_measurement(measurement)
        except ItemNotExistsError as e:
            logger.error(e)
            raise ValidationError(e)

        m_type = type(measurement)
        cls._data[m_type].remove(measurement)

        if not cls._data[m_type]:
            del cls._data[m_type]

        if measurement == cls._recent_measurement:
            cls._recent_measurement = cls._find_recent_measurement()

        cls._start_timestamp, cls._stop_timestamp = Updater.update_start_stop_on_removing(
            cls._data, measurement, cls._start_timestamp, cls._stop_timestamp
        )

    @classmethod
    def clear(cls) -> None:
        """Clears the storage."""
        cls._start_timestamp = None
        cls._stop_timestamp = None
        cls._recent_measurement = None
        cls._data.clear()

    @classmethod
    def _update_recent_measurement(cls, measurement: Measurement) -> None:
        """Updates the recent measurement in the storage by comparing the "stop"
        timestamp of measurement`s time range.

        Args:
            measurement: new measurement to compare with.
        """
        if (
            cls._recent_measurement is None
            or measurement.timestamp > cls._recent_measurement.timestamp
        ):
            cls._recent_measurement = measurement

    @classmethod
    def _find_recent_measurement(cls) -> Measurement | None:
        """Finds the measurement with the latest "stop" timestamp in the storage."""
        if not cls._data:
            return None

        recent_measurement = max(
            (measurement for measurements in cls._data.values() for measurement in measurements),
            key=lambda measurement: measurement.timestamp,
            default=None,
        )
        return recent_measurement

    @classmethod
    def _validate_new_measurement(cls, measurement: Measurement) -> None:
        """Validates a new measurement before adding.

        Args:
            measurement: a measurement to be added.

        Raises:
            ItemExistsError: if a measurement is already present in the storage.
        """
        m_type = type(measurement)

        if m_type in cls._data and measurement in cls._data[m_type]:
            raise ItemExistsError(f"Measurement {measurement} already exists in the storage.")

    @classmethod
    def _validate_removing_measurement(cls, measurement: Measurement) -> None:
        """Validates a measurement before removing.

        Args:
            measurement: a measurement to be removed.

        Raises:
            ItemNotExistsError: if a measurement is not present in the storage.
        """
        m_type = type(measurement)

        if m_type not in cls._data or measurement not in cls._data[m_type]:
            raise ItemNotExistsError(f"Measurement {measurement} does not exist in the storage.")
