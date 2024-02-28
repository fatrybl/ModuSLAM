from dataclasses import dataclass

from slam.setup_manager.sensors_factory.sensors import Sensor


@dataclass(frozen=True, eq=True)
class TimeRange:
    """Represents time range with start/stop timestamps."""

    start: int
    stop: int

    def __post_init__(self) -> None:

        assert self.start >= 0, f"timestamp start={self.start} can not be negative"
        assert self.stop >= 0, f"timestamp stop={self.stop} can not be negative"
        assert (
            self.start <= self.stop
        ), f"timestamp start={self.start} can not be greater than stop={self.stop}"


@dataclass(frozen=True, eq=True)
class PeriodicData:
    """Represents a periodic data request of a sensor."""

    sensor: Sensor
    period: TimeRange
