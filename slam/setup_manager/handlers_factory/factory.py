import logging

from slam.frontend_manager.handlers.ABC_handler import Handler
from slam.logger.logging_config import setup_manager
from slam.system_configs.setup_manager.handlers_factory import HandlersFactoryConfig
from slam.utils.auxiliary_methods import import_object
from slam.utils.exceptions import ItemNotFoundError

logger = logging.getLogger(setup_manager)


class HandlersFactory:
    """Creates and stores handlers."""

    _handlers = set[Handler]()

    @classmethod
    def get_handlers(cls) -> set[Handler]:
        """Gets all handlers."""
        return cls._handlers

    @classmethod
    def get_handler(cls, handler_name: str) -> Handler:
        """Gets handler with the given name.

        Args:
            handler_name: name of a handler.

        Returns:
            handler.

        Raises:
            ItemNotFoundError: if no handler with the given name is found.
        """
        for handler in cls._handlers:
            if handler.name == handler_name:
                return handler
        msg = f"No handler with name {handler_name!r} in {cls._handlers}"
        logger.critical(msg)
        raise ItemNotFoundError(msg)

    @classmethod
    def init_handlers(cls, config: HandlersFactoryConfig) -> None:
        """Initializes handlers for the given configuration by importing corresponding
        modules, objects and creating instances.

        Args:
            config: configuration of handlers.
        """
        cls._handlers.clear()

        package_name: str = config.package_name

        for name, cfg in config.handlers.items():
            module_name: str = cfg.module_name
            handler_object: type[Handler] = import_object(cfg.type_name, module_name, package_name)
            new_handler: Handler = handler_object(cfg)
            cls._handlers.add(new_handler)
