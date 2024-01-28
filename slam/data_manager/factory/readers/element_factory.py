from abc import ABC
from dataclasses import dataclass
from typing import Any

from slam.setup_manager.sensor_factory.sensors import Sensor


@dataclass(frozen=True)
class Location(ABC):
    """
    Abstract location to be inherited from.
    """


@dataclass(frozen=True)
class Measurement:
    """
    Sensor and its raw measurement.
    """

    sensor: Sensor
    values: tuple[Any, ...]

    def __hash__(self) -> int:
        return hash(self.sensor)


@dataclass(frozen=True)
class Element:
    """
    Element of a data batch.
    """

    timestamp: int
    measurement: Measurement
    location: Location
