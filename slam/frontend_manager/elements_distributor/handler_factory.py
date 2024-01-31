import logging
from importlib import import_module

from omegaconf import DictConfig

from slam.frontend_manager.handlers.ABC_handler import ElementHandler

logger = logging.getLogger(__name__)


class HandlerFactory:
    """
    Manages all handlers. Configure and setup sensor <-> handlers table.
    """

    def __init__(self, config: DictConfig) -> None:
        self._table = {}
        self._module_name: str = config.handlers_module
        self._package: str = config.handlers_package
        self._init_handlers(config)

    @property
    def sensor_handler_table(self):
        return self._table

    def _import_handler(self, instance_name: str) -> type[ElementHandler]:
        """
        Imports a handler with the given class name.
        Args:
            instance_name: name of handler`s class

        Returns:
            (type[ElementHandler]): subclass of base ElementHandler.
        """
        module = import_module(name=self._module_name, package=self._package)
        cls: type[ElementHandler] = getattr(module, instance_name)
        return cls

    def _init_handlers(self, config) -> None:
        """
        Initializes handlers with the given config.
        Args:
            config: sensor_name <-> handlers configurations.

        """
        for item in config:
            sensor_name: str = item.sensor_name
            self._table.update({sensor_name: []})

            for handler in item.handlers:
                instance_name: str = handler.instance
                try:
                    instance = self._import_handler(instance_name)
                except ImportError:
                    msg = f"Can not import handler with the the given instance name{instance_name}"
                    logger.error(msg)
                    raise
                else:
                    params = handler.parameters
                    new_handler = instance(config=params)
                    self._table[sensor_name].append(new_handler)
