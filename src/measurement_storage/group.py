from src.measurement_storage.measurements.base import Measurement


class MeasurementGroup:
    """Stores measurements of equal timestamps."""

    def __init__(self):
        self._measurements: set[Measurement] = set()

    @property
    def measurements(self) -> set[Measurement]:
        """Measurements of the group."""
        return self._measurements

    def add(self, measurement: Measurement):
        """Adds a measurement to the group."""
        self._measurements.add(measurement)

    def remove(self, measurement: Measurement):
        """Removes a measurement from the group."""
        self._measurements.remove(measurement)
