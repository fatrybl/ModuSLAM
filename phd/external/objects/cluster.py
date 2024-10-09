from moduslam.utils.auxiliary_dataclasses import TimeRange
from phd.external.metrics.utils import median
from phd.external.objects.measurements import ContinuousMeasurement, DiscreteMeasurement


class Cluster:
    """Stores measurements.

    TODO: make timestamp and time range properties calculation more efficient.
    """

    def __init__(self):
        self._discrete_measurements: list[DiscreteMeasurement] = []
        self._continuous_measurements: list[ContinuousMeasurement] = []
        self._timestamp: int | None = None
        self._time_range: TimeRange | None = None

    def __repr__(self):
        discrete_values = [m.value for m in self._discrete_measurements]
        connections_values = [m.value for m in self._continuous_measurements]
        return f"Cluster:{discrete_values + connections_values}"

    @property
    def timestamp(self) -> int:
        """Median timestamp of the cluster.

        Raises:
            ValueError: for empty cluster.
        """
        if self._timestamp:
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

    def add(self, measurement: DiscreteMeasurement | ContinuousMeasurement) -> None:
        """Adds new measurement to the cluster.

        Args:
            measurement: measurement to add.
        """
        if isinstance(measurement, DiscreteMeasurement):
            self._discrete_measurements.append(measurement)
            self._timestamp = self._compute_timestamp()
            self._time_range = self._compute_time_range()
        else:
            self._continuous_measurements.append(measurement)

    def _compute_timestamp(self) -> int:
        timestamps = [m.timestamp for m in self._discrete_measurements]
        return median(timestamps)

    def _compute_time_range(self) -> TimeRange:
        start = min((m.timestamp for m in self._discrete_measurements))
        stop = max((m.timestamp for m in self._discrete_measurements))
        return TimeRange(start, stop)
