from phd.bridge.objects.auxiliary_classes import FakeMeasurement
from phd.external.metrics.utils import median
from phd.measurements.processed_measurements import ContinuousMeasurement, Measurement
from phd.moduslam.utils.auxiliary_dataclasses import TimeRange


class Cluster:
    """Stores measurements.

    TODO: make timestamp and time range properties calculation more efficient.
          now it takes O(N*log(N)) cause of sorting.
    """

    def __init__(self):
        self._measurements: list[Measurement] = []
        self._continuous_measurements: list[ContinuousMeasurement] = []
        self._timestamp: int | None = None
        self._time_range: TimeRange | None = None

    def __repr__(self):
        return str(self._measurements + self._continuous_measurements)

    @property
    def is_empty(self) -> bool:
        """Checks if a cluster has measurements."""
        return len(self._measurements) + len(self._continuous_measurements) == 0

    @property
    def measurements(self) -> list[Measurement]:
        """All measurements in the cluster: core + fake + continuous."""
        return [*self._measurements, *self._continuous_measurements]

    @property
    def core_measurements(self) -> list[Measurement]:
        """Non-fake discrete measurements in the cluster."""
        cores = [m for m in self._measurements if not isinstance(m, FakeMeasurement)]
        return cores

    @property
    def continuous_measurements(self) -> list[ContinuousMeasurement]:
        """Continuous measurements in the cluster."""
        return self._continuous_measurements

    @property
    def fake_measurements(self) -> list[FakeMeasurement]:
        """Fake measurements in the cluster."""
        fakes = [m for m in self._measurements if isinstance(m, FakeMeasurement)]
        return fakes

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
        """
        if isinstance(measurement, ContinuousMeasurement):
            self._continuous_measurements.append(measurement)
            return

        self._measurements.append(measurement)
        self._timestamp = self._compute_timestamp()
        self._time_range = self._compute_time_range()

    def remove(self, measurement: Measurement) -> None:
        """Removes the measurement from the cluster.

        Args:
            measurement: measurement to be removed.
        """
        if isinstance(measurement, ContinuousMeasurement):
            self._continuous_measurements.remove(measurement)
            return

        self._measurements.remove(measurement)
        self._timestamp = self._compute_timestamp()
        self._time_range = self._compute_time_range()

    def _compute_timestamp(self) -> int | None:
        timestamps = sorted([m.timestamp for m in self._measurements])
        if timestamps:
            return median(timestamps)
        else:
            return None

    def _compute_time_range(self) -> TimeRange | None:
        if self._measurements:
            start = min((m.timestamp for m in self._measurements))
            stop = max((m.timestamp for m in self._measurements))
            return TimeRange(start, stop)
        else:
            return None
