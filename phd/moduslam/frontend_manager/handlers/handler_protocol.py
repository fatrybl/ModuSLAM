from typing import Protocol, runtime_checkable

from moduslam.data_manager.batch_factory.batch import Element
from moduslam.setup_manager.sensors_factory.sensors import Sensor
from phd.measurements.processed_measurements import Measurement


@runtime_checkable
class Handler(Protocol):
    @property
    def sensor_name(self) -> str:
        """Unique name of the handler."""

    @property
    def sensor_type(self) -> type[Sensor]:
        """Type of the sensor which measurements are processed with the handler."""

    @staticmethod
    def create_empty_element(element: Element) -> Element:
        """Creates an empty element with the same timestamp, location and sensor as the
        input element. Must be used in every Handler.

        Args:
            element: element of a data batch with raw data.

        Returns:
            empty element without raw data.
        """

    def process(self, element: Element) -> Measurement | None:
        """Processes the element.

        Args:
            element: element of a data batch to be processed.

        Returns:
            new measurement if created.
        """
