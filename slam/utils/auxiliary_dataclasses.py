from dataclasses import dataclass

from slam.setup_manager.sensors_factory.sensors import Sensor


@dataclass
class TimeRange:
    """
    Represents time range with start/stop timestamps.
    """

    start: int
    stop: int

    def __post_init__(self) -> None:
        if self.start > self.stop:
            msg = f"timestamp start={self.start} can not be greater than stop={self.stop}"
            raise ValueError(msg)

    def __hash__(self) -> int:
        return hash((self.start, self.stop))


@dataclass
class PeriodicData:
    """
    Represents a periodic data request of a sensor.
    """

    sensor: Sensor
    period: TimeRange

    def __hash__(self) -> int:
        return hash((self.period, self.sensor))
