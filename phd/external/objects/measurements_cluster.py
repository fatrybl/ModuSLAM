from moduslam.utils.auxiliary_dataclasses import TimeRange
from phd.external.metrics.utils import median
from phd.external.objects.measurements import (
    ContinuousMeasurement,
    CoreMeasurement,
    FakeMeasurement,
    Measurement,
)


class Cluster:
    """Stores measurements.

    TODO: make timestamp and time range properties calculation more efficient.
          now it takes O(n).
    """

    def __init__(self):
        self._core_measurements: list[CoreMeasurement] = []
        self._continuous_measurements: list[ContinuousMeasurement] = []
        self._fake_measurements: list[FakeMeasurement] = []
        self._timestamp: int | None = None
        self._time_range: TimeRange | None = None

    def __repr__(self):
        return str(
            self._core_measurements + self._continuous_measurements + self._fake_measurements
        )

    @property
    def is_empty(self) -> bool:
        """Checks if a cluster has measurements."""
        return (
            len(self._core_measurements)
            + len(self._continuous_measurements)
            + len(self._fake_measurements)
            == 0
        )

    @property
    def core_measurements(self) -> list[CoreMeasurement]:
        """Discrete measurements in the cluster."""
        return self._core_measurements

    @property
    def continuous_measurements(self) -> list[ContinuousMeasurement]:
        """Continuous measurements in the cluster."""
        return self._continuous_measurements

    @property
    def fake_measurements(self) -> list[FakeMeasurement]:
        """Fake measurements in the cluster."""
        return self._fake_measurements

    @property
    def measurements(self) -> list[CoreMeasurement | ContinuousMeasurement | FakeMeasurement]:
        """All measurement in the cluster."""
        return self._core_measurements + self._continuous_measurements + self._fake_measurements

    @property
    def timestamp(self) -> int:
        """Median timestamp of the cluster.

        Raises:
            ValueError: for empty cluster.
        """
        if self._timestamp is not None:
            return self._timestamp
        else:
            raise ValueError("Timestamp does not exist for empty cluster.")

    @property
    def time_range(self) -> TimeRange:
        """Time range of measurements inside the cluster.

        Raises:
            ValueError: for empty cluster.
        """
        if self._time_range:
            return self._time_range
        else:
            raise ValueError("Time range does not exist for empty cluster.")

    def add(self, measurement: Measurement) -> None:
        """Adds new measurement to the cluster.

        Args:
            measurement: measurement to add.

        Raises:
            TypeError: wrong type of measurement.
        """
        if isinstance(measurement, ContinuousMeasurement):
            self._continuous_measurements.append(measurement)

        elif isinstance(measurement, FakeMeasurement):
            self._fake_measurements.append(measurement)

        elif isinstance(measurement, CoreMeasurement):
            self._core_measurements.append(measurement)
            self._timestamp = self._compute_timestamp()
            self._time_range = self._compute_time_range()

        else:
            raise TypeError(f"Wrong type of measurement: {type(measurement)}")

    def remove(self, measurement: Measurement) -> None:
        """Removes the measurement from the cluster.

        Args:
            measurement: measurement to be removed.

        Raises:
            TypeError: wrong type of measurement.
        """
        if isinstance(measurement, CoreMeasurement):
            self._core_measurements.remove(measurement)
            self._timestamp = self._compute_timestamp()
            self._time_range = self._compute_time_range()

        elif isinstance(measurement, ContinuousMeasurement):
            self._continuous_measurements.remove(measurement)

        elif isinstance(measurement, FakeMeasurement):
            self._fake_measurements.remove(measurement)

        else:
            raise TypeError(f"Wrong type of measurement: {type(measurement)}")

    def _compute_timestamp(self) -> int | None:
        timestamps = [m.timestamp for m in self._core_measurements]
        if timestamps:
            return median(timestamps)
        else:
            return None

    def _compute_time_range(self) -> TimeRange | None:
        if self._core_measurements:
            start = min((m.timestamp for m in self._core_measurements))
            stop = max((m.timestamp for m in self._core_measurements))
            return TimeRange(start, stop)
        else:
            return None
