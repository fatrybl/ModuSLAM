from typing import Any

from phd.measurements.processed_measurements import Measurement, PoseOdometry
from phd.moduslam.data_manager.batch_factory.batch import Element


class SplitPoseOdometry(Measurement):
    def __init__(self, timestamp: int, parent: PoseOdometry):
        self._timestamp = timestamp
        self._parent = parent

    def __repr__(self):
        return f"split odom:{self._timestamp}"

    @property
    def timestamp(self) -> int:
        return self._timestamp

    @property
    def elements(self) -> list[Element]:
        return self._parent.elements

    @property
    def parent(self) -> PoseOdometry:
        return self._parent


class PseudoMeasurement(Measurement):
    """Pseudo measurement with timestamp and value.

    Does not contain data batch elements.
    """

    def __init__(self, timestamp: int, value: Any = "some value"):
        self._timestamp = timestamp
        self._value = value

    def __repr__(self):
        return f"pseudo at:{self._timestamp}"

    @property
    def timestamp(self) -> int:
        return self._timestamp

    @property
    def elements(self) -> list[Element]:
        return []

    @property
    def value(self) -> Any:
        return self._value


class FakeMeasurement(Measurement):

    def __init__(self, timestamp: int):
        self._timestamp = timestamp

    def __repr__(self) -> str:
        return "fake"

    @property
    def timestamp(self) -> int:
        return self._timestamp

    @property
    def elements(self) -> list[Element]:
        return []

    @property
    def value(self) -> str:
        return "fake"


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
