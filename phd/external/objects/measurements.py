from typing import Any, Protocol, runtime_checkable

from moduslam.utils.auxiliary_dataclasses import TimeRange


@runtime_checkable
class Measurement(Protocol):
    """Any discrete measurement."""

    @property
    def timestamp(self) -> int: ...

    @property
    def value(self) -> Any: ...


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
    """Any non-core measurement (aka IMU)."""

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

    fake_value: str = "Fake"

    def __init__(self, timestamp: int):
        self._timestamp = timestamp
        self._value = self.fake_value

    def __repr__(self):
        return self.fake_value

    @property
    def timestamp(self) -> int:
        return self._timestamp

    @property
    def value(self) -> str:
        return self._value
