from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from src.measurement_storage.measurements.base import Measurement
from src.moduslam.data_manager.batch_factory.batch import Element
from src.moduslam.sensors_factory.sensors import Sensor


@dataclass
class HandlerConfig:
    """Base handler configuration."""

    sensor_name: str  # name of a sensor which data is processed.


@runtime_checkable
class Handler(Protocol):
    @property
    def sensor_name(self) -> str:
        """Unique name of the handler."""

    @property
    def sensor_type(self) -> type[Sensor]:
        """Type of the sensor which measurements are processed with the handler."""

    def process(self, element: Element) -> Measurement | None:
        """Processes the element.

        Args:
            element: element of a data batch to be processed.

        Returns:
            new measurement if created.
        """
