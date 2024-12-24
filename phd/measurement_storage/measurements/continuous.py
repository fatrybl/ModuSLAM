from typing import Generic, TypeVar

from phd.measurement_storage.measurements.base import Measurement, TimeRangeMeasurement
from phd.utils.auxiliary_dataclasses import TimeRange

M = TypeVar("M", bound=Measurement, covariant=True)


class ContinuousMeasurement(Generic[M], TimeRangeMeasurement):
    """A measurement consisting of multiple measurements."""

    def __init__(self, measurements: list[M]):
        """
        Args:
            measurements: sorted by timestamp measurements.
        """

        if len(measurements) == 0:
            raise ValueError("Not enough elements to create a measurement.")

        start = measurements[0].timestamp
        stop = measurements[-1].timestamp
        self._timestamp = stop
        self._time_range = TimeRange(start, stop)
        self._items = measurements

    def __repr__(self):
        return f"Continuous with: {len(self._items)} elements"

    @property
    def timestamp(self) -> int:
        """The timestamp of the continuous measurement."""
        return self._timestamp

    @property
    def time_range(self) -> TimeRange:
        """The time range of the continuous measurement."""
        return self._time_range

    @property
    def items(self) -> list[M]:
        """Discrete items of the continuous measurement."""
        return self._items
