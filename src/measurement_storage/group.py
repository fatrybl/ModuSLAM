from src.measurement_storage.measurements.base import Measurement


class MeasurementGroup:
    """Stores measurements of equal timestamps."""

    def __init__(self):
        self._measurements: set[Measurement] = set()
        self._timestamp: int | None = None

    @property
    def timestamp(self) -> int:
        """Timestamp of the group.

        Raises:
            ValueError: for empty group.
        """
        if self._timestamp is not None:
            return self._timestamp

        raise ValueError("Timestamp does not exist for empty group.")

    @property
    def measurements(self) -> set[Measurement]:
        """Measurements in the group."""
        return self._measurements

    def add(self, measurement: Measurement):
        """Adds a measurement to the group."""
        if self._timestamp is not None and self._timestamp != measurement.timestamp:
            raise ValueError("Group must contain measurements with equal timestamps.")

        self._measurements.add(measurement)

    def remove(self, measurement: Measurement):
        """Removes a measurement from the group."""
        self._measurements.remove(measurement)
        if not self._measurements:
            self._timestamp = None
