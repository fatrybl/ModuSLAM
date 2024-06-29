from dataclasses import dataclass
from typing import Any

from moduslam.data_manager.batch_factory.readers.locations import Location
from moduslam.setup_manager.sensors_factory.sensors import Sensor


@dataclass(frozen=True, eq=True)
class RawMeasurement:
    """Raw sensor measurement.

    Hash() calculation ignores values because some of them might not be hashable, i.e.
    PIL.Image.
    """

    sensor: Sensor
    values: Any

    def __hash__(self) -> int:
        return hash(self.sensor)


@dataclass(frozen=True, eq=True)
class Element:
    """Element of a data batch."""

    timestamp: int
    measurement: RawMeasurement
    location: Location
