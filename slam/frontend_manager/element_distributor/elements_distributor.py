import logging
from typing import Iterable

from slam.data_manager.factory.batch import DataBatch
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
        self.storage = MeasurementStorage()
        self._table: dict[Sensor, list[Handler]] = {}

    def init_table(self, table_config: dict[str, list[str]]) -> None:
        """Initializes sensor-handler table.

        Args:
            table_config (dict[str, list[str]]): table with sensor names as key and list of handler names as values.
        """
        self._table = init_sensor_handler_table(table_config)

    @property
    def sensor_handler_table(self) -> dict[Sensor, list[Handler]]:
        """Represents connections between sensors and handlers.

        Returns:
            (dict[Sensor, list[ElementHandler]]): table with sensor names as key and list of handlers as values.
        """
        return self._table

    def clear_storage(self, data: Iterable[OrderedSet[Measurement]]) -> None:
        for ordered_set in data:
            for measurement in ordered_set:
                self.storage.remove(measurement)

    def distribute_next(self, data_batch: DataBatch) -> None:
        """Takes element from the data batch and process it with external module.

        1) Gets recent element from DataBatch.
        2) Distributes it to the corresponding handler.
        3) Updates measurement storage if a new measurement has been created by the handler.

        TODO: add support for multiple args for process() method.
        Returns:
            measurement: processed element as measurement.
        """
        element: Element = data_batch.first
        handlers = self.sensor_handler_table[element.measurement.sensor]

        for handler in handlers:
            z: Measurement | None = handler.process(element)
            if z:
                self.storage.add(z)
