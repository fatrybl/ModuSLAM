import logging

from omegaconf import DictConfig

from slam.data_manager.factory.batch import DataBatch
from slam.data_manager.factory.readers.element_factory import Element
from slam.frontend_manager.elements_distributor.handler_factory import HandlerFactory
from slam.frontend_manager.elements_distributor.measurement_storage import (
    Measurement,
    MeasurementStorage,
)
from slam.frontend_manager.handlers.ABC_handler import Handler
from slam.setup_manager.sensor_factory.sensors import Sensor

logger = logging.getLogger(__name__)


class ElementDistributor:
    """
    Distributes elements from DataBatch to corresponding external modules for preprocessing.
    """

    def __init__(self, config: DictConfig):
        self.handler_factory = HandlerFactory(config.handler_factory)
        self.storage = MeasurementStorage()
        self._table: dict[Sensor, list[Handler]] = self.handler_factory.sensor_handler_table

    def _distribute(self, element: Element) -> None:
        sensor: Sensor = element.measurement.sensor
        handlers = self._table[sensor]
        for handler in handlers:
            z: Measurement | None = handler.process(element)
            if z is not None:
                self.storage.add(handler, z)

    def next_element(self, data_batch: DataBatch):
        """
        Takes element from DataBatch and process it with external module.

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
