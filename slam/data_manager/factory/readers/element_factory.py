from abc import ABC
from dataclasses import dataclass
from typing import Any, Type

from slam.setup_manager.sensor_factory.sensors import Sensor


@dataclass(frozen=True)
class Location(ABC):
    """
    Abstract location for inheritence of
    """


@dataclass
class Measurement:
    sensor: Type[Sensor]
    values: Any


@dataclass
class Element:
    timestamp: int
    measurement: Measurement
    location: Type[Location]
