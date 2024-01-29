import logging

from slam.data_manager.factory.batch import DataBatch
from slam.data_manager.factory.readers.element_factory import Element
from slam.frontend_manager.elements_distributor.handler_factory import HandlerFactory
from slam.frontend_manager.elements_distributor.measurement_storage import (
    Measurement,
    MeasurementStorage,
)

logger = logging.getLogger(__name__)


class ElementDistributor:
    """
    Distributes elements from DataBatch to corresponding external modules for preprocessing.
    """

    def __init__(self, config):
        self.handler_factory = HandlerFactory()
        self.storage = MeasurementStorage()

    def _distribute(self, element: Element) -> None:
        sensor_name: str = element.measurement.sensor.name
        handlers = self.handler_factory.sensor_handler_table[sensor_name]
        for handler in handlers:
            z: Measurement | None = handler.process(element)
            if z:
                self.storage.add(handler, z)

    def next_element(self, data_batch: DataBatch):
        """
        API function to get next element from DataBatch and process it with external module.

        TODO:
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
