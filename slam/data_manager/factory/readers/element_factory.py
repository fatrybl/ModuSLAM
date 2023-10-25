from abc import ABC
from dataclasses import dataclass
from typing import Any, Type

from slam.setup_manager.sensor_factory.sensors import Sensor


@dataclass(frozen=True)
class Location(ABC):
    """
    Abstract location for inheritence of
    """


@dataclass(frozen=True)
class Measurement:
    sensor: Type[Sensor]
    values: tuple[Any]

    def __hash__(self) -> int:
        return hash(self.sensor)


@dataclass(frozen=True)
class Element:
    timestamp: int
    measurement: Measurement
    location: Type[Location]
