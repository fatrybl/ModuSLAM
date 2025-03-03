from src.external.metrics.utils import median
from src.measurement_storage.measurements.auxiliary import FakeMeasurement
from src.measurement_storage.measurements.base import Measurement
from src.measurement_storage.measurements.continuous import ContinuousMeasurement
from src.utils.auxiliary_dataclasses import TimeRange
from src.utils.exceptions import ItemExistsError, ItemNotExistsError, ValidationError
from src.utils.ordered_set import OrderedSet


class MeasurementCluster:
    """Stores measurements.

    TODO:
        1. make timestamp and time range properties calculation more efficient.
           now it takes O(N*log(N)) cause of sorting.
        2. measurements property always returns core measurements first loosing the insertion order.
    """

    def __init__(self):
        self._core_measurements: dict[int, set[Measurement]] = {}
        self._continuous_measurements = OrderedSet[ContinuousMeasurement]()
        self._timestamp: int | None = None
        self._time_range: TimeRange | None = None

    def __contains__(self, item) -> bool:
        return (
            any(item in measurements for measurements in self._core_measurements.values())
            or item in self._continuous_measurements
        )

    def __repr__(self):
        number = len(self._core_measurements) + len(self._continuous_measurements)
        return f"Cluster with {number} measurements."

    @property
    def empty(self) -> bool:
        """Checks if a cluster has measurements."""
        return not bool(self._continuous_measurements) and not bool(self._core_measurements)

    @property
    def measurements(self) -> tuple[Measurement, ...]:
        """All measurements in the cluster: core + fake + continuous."""
        tup1 = tuple(m for measurements in self._core_measurements.values() for m in measurements)
        tup2 = tuple(self._continuous_measurements)
        return tup1 + tup2

    @property
    def core_measurements(self) -> tuple[Measurement, ...]:
        """Non-fake discrete measurements in the cluster."""
        cores = tuple(
            m
            for measurements in self._core_measurements.values()
            for m in measurements
            if not isinstance(m, FakeMeasurement)
        )
        return cores

    @property
    def continuous_measurements(self) -> tuple[ContinuousMeasurement, ...]:
        """Continuous measurements in the cluster."""
        return tuple(self._continuous_measurements.items)

    @property
    def fake_measurements(self) -> tuple[FakeMeasurement, ...]:
        """Fake measurements in the cluster.
        They are not used to compute time properties of the cluster."""
        fakes = tuple(
            m
            for measurements in self._core_measurements.values()
            for m in measurements
            if isinstance(m, FakeMeasurement)
        )
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
        """Time range of measurements in the cluster.

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
            ValidationError: if measurement is already present in the cluster.
        """
        try:
            self._validate_new_measurement(measurement)
        except ItemExistsError as e:
            raise ValidationError(e)

        if isinstance(measurement, ContinuousMeasurement):
            self._continuous_measurements.add(measurement)
            return

        t = measurement.timestamp
        if t not in self._core_measurements:
            self._core_measurements[t] = set()

        self._core_measurements[t].add(measurement)
        self._timestamp = self._compute_timestamp()
        self._time_range = self._compute_time_range()

    def remove(self, measurement: Measurement) -> None:
        """Removes the measurement from the cluster.

        Args:
            measurement: measurement to be removed.

        Raises:
            ValueError: if measurement is not present in the cluster.
        """
        try:
            self._validate_removing_measurement(measurement)
        except ItemNotExistsError as e:
            raise ValidationError(e)

        if isinstance(measurement, ContinuousMeasurement):
            self._continuous_measurements.remove(measurement)
            return

        t = measurement.timestamp
        self._core_measurements[t].remove(measurement)
        if not self._core_measurements[t]:
            del self._core_measurements[t]

        self._timestamp = self._compute_timestamp()
        self._time_range = self._compute_time_range()

    def _validate_new_measurement(self, measurement: Measurement):
        """Validates a new measurement before adding.

        Args:
            measurement: a measurement to be added.

        Raises:
            ItemExistsError: if a measurement is already present in the cluster.
        """
        t = measurement.timestamp
        if (
            t in self._core_measurements and measurement in self._core_measurements[t]
        ) or measurement in self._continuous_measurements:
            raise ItemExistsError(f"Measurement {measurement} already exists in the cluster.")

    def _validate_removing_measurement(self, measurement: Measurement):
        """Validates a measurement before removing.

        Args:
            measurement: a measurement to be removed.

        Raises:
            ItemNotExistsError: if a measurement is not present in the cluster.
        """
        t = measurement.timestamp
        if (
            t not in self._core_measurements or measurement not in self._core_measurements[t]
        ) and measurement not in self._continuous_measurements:
            raise ItemNotExistsError(f"Measurement {measurement} is not present in the cluster.")

    def _compute_timestamp(self) -> int | None:
        """Computes timestamp of the cluster as a median time of sorted measurements.

        Returns:
            median timestamp or None if no measurements.
        """
        timestamps = sorted(self._core_measurements.keys())
        if timestamps:
            return median(timestamps)
        else:
            return None

    def _compute_time_range(self) -> TimeRange | None:
        """Computes time range of the cluster.

        Returns:
            time range or None if no measurements.
        """
        if self._core_measurements:
            start = min(self._core_measurements.keys())
            stop = max(self._core_measurements.keys())
            return TimeRange(start, stop)
        else:
            return None
