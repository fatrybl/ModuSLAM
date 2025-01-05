from src.measurement_storage.measurements.base import Measurement


class MeasurementGroup:
    """Stores measurements of equal timestamps."""

    def __init__(self):
        self._measurements: set[Measurement] = set()

    @property
    def measurements(self) -> set[Measurement]:
        return self._measurements

    def add(self, measurement: Measurement):
        self._measurements.add(measurement)

    def remove(self, measurement: Measurement):
        self._measurements.remove(measurement)
