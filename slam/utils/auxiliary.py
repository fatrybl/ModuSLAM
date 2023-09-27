from typing import Type
from dataclasses import dataclass
from slam.setup_manager.sensor_factory.sensors import Sensor


@dataclass
class TimeLimit:
    start: int
    stop: int

    def __post_init__(self) -> None:
        if self.start > self.stop:
            msg = f"timestamp start={self.start} can not be greater than stop={self.stop}"
            raise ValueError(msg)

    def __hash__(self) -> int:
        return hash((self.start, self.stop))


@dataclass
class SensorData:
    sensor: Type[Sensor]
    period: TimeLimit

    def __hash__(self) -> int:
        return hash((self.period, self.sensor))
