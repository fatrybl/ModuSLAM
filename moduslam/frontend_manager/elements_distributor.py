from typing import Iterable

from moduslam.data_manager.batch_factory.batch import Element
from moduslam.frontend_manager.handlers.interface import Handler
from moduslam.frontend_manager.measurement_storage import (
    Measurement,
    MeasurementStorage,
)
from moduslam.setup_manager.sensors_factory.sensors import Sensor
from moduslam.setup_manager.tables_initializer import init_sensor_handler_table
from moduslam.utils.ordered_set import OrderedSet


class ElementDistributor:
    """Distributes elements from DataBatch to corresponding handlers for further
    processing."""

    def __init__(self):
        self._storage = MeasurementStorage()
        self._table: dict[Sensor, list[Handler]] = {}

    @property
    def storage(self) -> MeasurementStorage:
        """Storage of measurements."""
        return self._storage

    @property
    def sensor_handler_table(self) -> dict[Sensor, list[Handler]]:
        """ "Sensor -> handlers" tables."""
        return self._table

    def init_table(self, table_config: dict[str, list[str]]) -> None:
        """Initializes "sensor -> handlers" table.

        Args:
            table_config: table with "sensor name -> handlers names" pairs.
        """
        self._table = init_sensor_handler_table(table_config)

    def clear_storage(self, data: Iterable[OrderedSet[Measurement]]) -> None:
        """Removes the given data from the measurements storage.

        Args:
            data: data to be removed from storage.
        """
        for ordered_set in data:
            for measurement in ordered_set:
                self.storage.remove(measurement)

    def distribute_element(self, element: Element) -> None:
        """Distributes the element to the handler for further processing."""
        handlers = self.sensor_handler_table[element.measurement.sensor]

        for handler in handlers:
            m: Measurement | None = handler.process(element)
            if m:
                self.storage.add(m)
