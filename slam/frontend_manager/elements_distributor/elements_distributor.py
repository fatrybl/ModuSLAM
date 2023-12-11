import logging
from collections import deque
from typing import Type

from slam.data_manager.factory.batch import DataBatch
from slam.data_manager.factory.readers.element_factory import Element
from slam.frontend_manager.elements_distributor.measurement import Measurement
from slam.frontend_manager.elements_distributor.sensor_handler_table import sensor_handler_table
from slam.frontend_manager.handlers.ABC_module import ElementHandler
from slam.frontend_manager.handlers.imu_preintegration.imu_preintegration import ImuPreintegration
from slam.frontend_manager.handlers.pointcloid_registration.pointcloud_matcher import KissICP
from slam.setup_manager.sensor_factory.sensor_factory import SensorFactory
from slam.setup_manager.sensor_factory.sensors import Sensor

logger = logging.getLogger(__name__)


class MeasurementStorage:
    def __init__(self, modules: tuple[Type[ElementHandler], ...]) -> None:
        self.data: dict[Type[ElementHandler], deque[Measurement]] = {
            m: deque() for m in modules}

    def delete(self, module: Type[ElementHandler], z: Measurement) -> None:
        """
        Deletes the measurement from the storage.
        Args:
            z (Measurement): The measurement to be deleted.
        """
        self.data[module].remove(z)
        pass

    def add(self, module: Type[ElementHandler], z: Measurement) -> None:
        """
        Adds a new measurement to the storage.
        Args:
            module (ElementHandler): an external module object which creates the measurement.
            z (Measurement): a new measurement to be added.
        """
        self.data[module].append(z)


class ElementDistributor:
    """
    Distributes elements from DataBatch to corresponding external modules for preprocessing.
    """

    def __init__(self, config):
        self.lidar_odom = KissICP()
        self.imu_odom = ImuPreintegration()
        self.external_modules: tuple[Type[ElementHandler], ...] = (
            self.lidar_odom,
            self.imu_odom)
        self.storage = MeasurementStorage(self.external_modules)
        self._init_table()

    def _init_table(self) -> None:
        """
        Initializes the table(dictionary) with Sensor -> Modules pairs.
        """
        self._table: dict[Type[Sensor], list[Type[ElementHandler]]] = {}
        for sensor in SensorFactory.used_sensors:
            sensor_type = type(sensor)
            modules_types = sensor_handler_table[sensor_type]
            modules: list[Type[ElementHandler]] = []
            for module in self.external_modules:
                for m_type in modules_types:
                    if isinstance(module, m_type):
                        modules.append(module)
            if len(modules) != 0:
                self._table.update({sensor_type: modules})
        if len(self._table.keys()) == 0:
            msg = f"No modules in Sensor-Modules table: {self._table} for used sensors: {SensorFactory.used_sensors}"
            logger.critical(msg)
            raise KeyError

    def _distribute(self, element: Element) -> None:
        handlers = self._table[element.measurement.sensor]
        for handler in handlers:
            z: Measurement = handler.process(element)
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
