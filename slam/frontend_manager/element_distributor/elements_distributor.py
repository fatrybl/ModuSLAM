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
from slam.system_configs.system.frontend_manager.element_distributor.element_distributor import (
    ElementDistributorConfig,
)
from slam.utils.ordered_set import OrderedSet

logger = logging.getLogger(__name__)


class ElementDistributor:
    """Distributes elements from DataBatch to corresponding handlers for
    preprocessing."""

    def __init__(self, config: ElementDistributorConfig):
        self.storage = MeasurementStorage()
        self._table: dict[Sensor, list[Handler]] = init_sensor_handler_table(
            config.sensor_handlers_table
        )

    def _distribute(self, element: Element) -> None:
        """Distributes element to corresponding handler based on sensor.

        Args:
            element (Element): element from DataBatch.

        TODO: add support for multiple args for process() method.
        """
        handlers = self._table[element.measurement.sensor]
        for handler in handlers:
            z: Measurement | None = handler.process(element)
            if z:
                self.storage.add(z)

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

    def next_element(self, data_batch: DataBatch) -> None:
        """Takes element from DataBatch and process it with external module.

        1) Gets last element from DataBatch.
        2) Processes it with a corresponding handler.
        3) Updates measurement storage.
        4) Remove element from DataBatch.

        Returns:
            measurement: processed element as measurement.
        """
        element: Element = data_batch.first
        self._distribute(element)
