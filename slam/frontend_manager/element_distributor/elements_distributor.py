import logging
from typing import Iterable

from slam.data_manager.factory.element import Element
from slam.frontend_manager.element_distributor.measurement_storage import (
    Measurement,
    MeasurementStorage,
)
from slam.frontend_manager.handlers.ABC_handler import Handler
from slam.setup_manager.sensors_factory.sensors import Sensor
from slam.setup_manager.tables_initializer import init_sensor_handler_table
from slam.utils.ordered_set import OrderedSet

logger = logging.getLogger(__name__)


class ElementDistributor:
    """Distributes elements from DataBatch to corresponding handlers for
    preprocessing."""

    def __init__(self):
        self._storage = MeasurementStorage()
        self._table: dict[Sensor, list[Handler]] = {}

    @property
    def storage(self) -> MeasurementStorage:
        """Storage of measurements.

        Returns:
            storage of measurements (MeasurementStorage).
        """
        return self._storage

    def init_table(self, table_config: dict[str, list[str]]) -> None:
        """Initializes sensor-handler table.

        Args:
            table_config (dict[str, list[str]]): table with sensor names as key and list of handler names as values.
        """
        self._table = init_sensor_handler_table(table_config)

    @property
    def sensor_handler_table(self) -> dict[Sensor, list[Handler]]:
        """Table with connections between sensors and handlers.

        Returns:
            Sensor -> handlers table (dict[Sensor, list[Handler]]).
        """
        return self._table

    def clear_storage(self, data: Iterable[OrderedSet[Measurement]]) -> None:
        """Clears the storage from measurements.

        Args:
            data (Iterable[OrderedSet[Measurement]]): data to be removed from storage.
        """
        for ordered_set in data:
            for measurement in ordered_set:
                self.storage.remove(measurement)

    def distribute_element(self, element: Element) -> None:
        """Distributes an element to the handler for processing.

        TODO: add support for multiple args for process() method.
        Returns:
            measurement: processed element as measurement.
        """
        handlers = self.sensor_handler_table[element.measurement.sensor]

        for handler in handlers:
            m: Measurement | None = handler.process(element)
            if m:
                self.storage.add(m)
