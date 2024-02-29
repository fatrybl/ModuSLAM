from dataclasses import dataclass

from slam.setup_manager.sensors_factory.sensors import Sensor


@dataclass(frozen=True, eq=True)
class Location:
    """Abstract location to be inherited from."""


@dataclass(frozen=True, eq=True)
class Measurement:
    """Sensor and its raw measurement."""

    sensor: Sensor
    values: tuple

    def __hash__(self) -> int:
        return hash(self.sensor)


@dataclass(frozen=True, eq=True)
class Element:
    """Element of a data batch."""

    timestamp: int
    measurement: Measurement
    location: Location
