from typing import Any, Protocol, TypeVar, runtime_checkable

from moduslam.utils.auxiliary_dataclasses import TimeRange


@runtime_checkable
class Measurement(Protocol):
    """Any discrete measurement."""

    @property
    def timestamp(self) -> int:
        """Timestamp of the measurement."""

    @property
    def value(self) -> Any:
        """Value of the measurement."""


T = TypeVar("T", bound=Measurement)


class MeasurementGroup:
    """Stores measurements of equal timestamps."""

    def __init__(self):
        self._measurements: list[Measurement] = []

    @property
    def measurements(self) -> list[Measurement]:
        return self._measurements

    def add(self, measurement: Measurement):
        self._measurements.append(measurement)

    def remove(self, measurement: Measurement):
        self._measurements.remove(measurement)


class CoreMeasurement(Measurement):
    """Any discrete measurement."""

    def __init__(self, timestamp: int, value: Any):
        self._timestamp = timestamp
        self._value = value

    def __repr__(self):
        return str(self._value)

    @property
    def timestamp(self) -> int:
        return self._timestamp

    @property
    def value(self) -> Any:
        return self._value


class ContinuousMeasurement(Measurement):
    """A pre-integratable measurement."""

    def __init__(self, elements: list[CoreMeasurement]):

        if len(elements) == 0:
            raise ValueError("Not enough elements to create a measurement.")

        start = elements[0].timestamp
        stop = elements[-1].timestamp
        self._timestamp = stop
        self._value = sum((el.value for el in elements))
        self._time_range = TimeRange(start, stop)
        self._elements = elements

    def __repr__(self):
        return f"num elements: {len(self._elements)}"

    @property
    def timestamp(self) -> int:
        return self._timestamp

    @property
    def time_range(self) -> TimeRange:
        return self._time_range

    @property
    def value(self) -> Any:
        return self._value

    @property
    def elements(self) -> list[CoreMeasurement]:
        return self._elements


class FakeMeasurement(Measurement):

    fake_value: str = "fake"

    def __init__(self, timestamp: int):
        self._timestamp = timestamp

    def __repr__(self):
        return self.fake_value

    @property
    def timestamp(self) -> int:
        return self._timestamp

    @property
    def value(self) -> str:
        return self.fake_value


class Odometry(Measurement):

    def __init__(self, start: int, stop: int, value: Any):
        self._time_range = TimeRange(start, stop)
        self._value = value

    def __repr__(self):
        return f"{self._time_range.start}-{self._time_range.stop}"

    @property
    def timestamp(self) -> int:
        return self._time_range.stop

    @property
    def time_range(self) -> TimeRange:
        return self._time_range

    @property
    def value(self) -> Any:
        return self._value


class SplittedOdometry(CoreMeasurement):
    def __init__(self, timestamp: int, value: Any, parent: Odometry):
        super().__init__(timestamp, value)
        self._parent = parent

    def __repr__(self):
        return f"odom:{self._timestamp}"

    @property
    def parent(self) -> Odometry:
        return self._parent
