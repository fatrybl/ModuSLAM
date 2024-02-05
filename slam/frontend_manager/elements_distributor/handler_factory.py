import logging
from importlib import import_module

from omegaconf import DictConfig

from slam.frontend_manager.handlers.ABC_handler import Handler
from slam.setup_manager.sensor_factory.sensor_factory import SensorFactory
from slam.setup_manager.sensor_factory.sensors import Sensor

logger = logging.getLogger(__name__)


class HandlerFactory:
    """
    Creates handlers.
    """

    handlers = set[Handler]()

    def __init__(self, config: DictConfig) -> None:
        self._sensor_handlers_pairs: list = config.pairs
        self._module_name: str = config.handlers_module
        self._package: str = config.handlers_package
        self._table: dict[Sensor, list[Handler]] = {}
        self._init_handlers()

    @property
    def sensor_handler_table(self) -> dict[Sensor, list[Handler]]:
        """
        Represents connections between sensors and handlers.
        Measurements from the sensor will be processed by the handlers.
        Returns:
            (dict[Sensor, list[ElementHandler]]): table with sensor names as keys and handlers as values.
        """
        return self._table

    def _import_handler(self, object_name: str) -> type[Handler]:
        """
        Imports a handler with the given class name.
        Args:
            object_name: name of handler`s class

        Returns:
            (type[Handler]): subclass of base Handler.
        """
        module = import_module(name=self._module_name, package=self._package)
        cls: type[Handler] = getattr(module, object_name)
        return cls

    def _init_handlers(self) -> None:
        """
        Initializes handlers with the given config.
        Args:
            self._sensor_handlers_pairs:
                    "sensor_name": list ["handler_name", ...].

                    "imu1": ["Imu1Handler", "StereocameraHandler"]
                    "stereo_camera": ["StereocameraHandler", "KeyPointsHandler"]

        """
        for pair in self._sensor_handlers_pairs:
            sensor_name: str = pair.sensor_name
            handlers: list = pair.handlers
            sensor: Sensor = SensorFactory.name_to_sensor(sensor_name)
            self._table[sensor] = []

            for handler in handlers:
                object_name: str = handler.object
                try:
                    instance = self._import_handler(object_name)
                except KeyError:
                    msg = f"Can not import handler with the the given object name{object_name!r}"
                    logger.error(msg)
                    raise
                else:
                    handler = instance(config=handler.parameters)
                    self.handlers.add(handler)
                    self._table[sensor].append(handler)
