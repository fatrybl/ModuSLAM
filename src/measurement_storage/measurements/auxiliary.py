"""Auxiliary measurements used for different purposes."""

from typing import Any

from src.measurement_storage.measurements.base import Measurement
from src.measurement_storage.measurements.pose_odometry import Odometry


class SplitPoseOdometry(Measurement):
    def __init__(self, timestamp: int, parent: Odometry):
        self._timestamp = timestamp
        self._parent = parent

    def __repr__(self):
        return f"split odom:{self._timestamp}"

    @property
    def timestamp(self) -> int:
        return self._timestamp

    @property
    def parent(self) -> Odometry:
        return self._parent


class PseudoMeasurement(Measurement):
    """Pseudo measurement with timestamp and value."""

    def __init__(self, timestamp: int, value: Any = "some value"):
        self._timestamp = timestamp
        self._value = value

    def __repr__(self):
        return f"pseudo at:{self._timestamp}"

    @property
    def timestamp(self) -> int:
        return self._timestamp

    @property
    def value(self) -> Any:
        """Value of the measurement."""
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
    def value(self) -> str:
        return "fake"
