import logging

from system_configs.system.frontend_manager.element_distributor.element_distributor import (
    ElementDistributorConfig,
)

from slam.data_manager.factory.batch import DataBatch
from slam.data_manager.factory.element import Element
from slam.frontend_manager.element_distributor.measurement_storage import (
    Measurement,
    MeasurementStorage,
)
from slam.frontend_manager.handlers.ABC_handler import Handler
from slam.setup_manager.handlers_factory.factory import HandlerFactory
from slam.setup_manager.sensors_factory.factory import SensorFactory
from slam.setup_manager.sensors_factory.sensors import Sensor

logger = logging.getLogger(__name__)


class ElementDistributor:
    """Distributes elements from DataBatch to corresponding handlers for
    preprocessing."""

    def __init__(self, config: ElementDistributorConfig):
        self.storage = MeasurementStorage()
        self._table: dict[Sensor, list[Handler]] = {}
        self._fill_table(config.sensor_handlers_table)

    def _fill_table(self, config: dict[str, list[str]]) -> None:
        """Fills sensor-handler table."""
        for sensor_name, handlers_names in config.items():
            sensor: Sensor = SensorFactory.get_sensor(sensor_name)
            handlers = [HandlerFactory.get_handler(name) for name in handlers_names]
            self._table[sensor] = handlers

    def _distribute(self, element: Element) -> None:
        """Distributes element to corresponding handler based on sensor.

        Args:
            element (Element): element from DataBatch.
        """
        sensor: Sensor = element.measurement.sensor
        handlers = self._table[sensor]
        for handler in handlers:
            z: Measurement | None = handler.process(element)
            if z is not None:
                self.storage.add(handler, z)

    @property
    def sensor_handler_table(self) -> dict[Sensor, list[Handler]]:
        """Represents connections between sensors and handlers.

        Returns:
            (dict[Sensor, list[ElementHandler]]): table with sensor names as key and list of handlers as values.
        """
        return self._table

    def next_element(self, data_batch: DataBatch) -> None:
        """Takes element from DataBatch and process it with external module.

        1) Gets last element from DataBatch.
        2) Processes it with a corresponding handler.
        3) Updates measurement storage.
        4) Remove element from DataBatch.

        Returns:
            measurement: processed element as measurement.
        """
        element: Element = data_batch.first_element
        self._distribute(element)
        data_batch.delete_first()
