from dataclasses import dataclass
from typing import Any

from slam.data_manager.factory.readers.kaist.auxiliary_classes import Location
from slam.setup_manager.sensors_factory.sensors import Sensor


@dataclass(frozen=True, eq=True)
class RawMeasurement:
    """Sensor and its raw measurement.

    Hash() calculation ignores values because some of them might not be hashable, i.e.
    PIL.Image .
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
