import logging

from slam.frontend_manager.handlers.ABC_handler import Handler
from slam.system_configs.system.setup_manager.handlers_factory import (
    HandlersFactoryConfig,
)
from slam.utils.auxiliary_methods import import_object
from slam.utils.exceptions import ItemNotFoundError

logger = logging.getLogger(__name__)


class HandlerFactory:
    """Creates handlers."""

    _handlers = set[Handler]()

    @classmethod
    def get_handlers(cls) -> set[Handler]:
        """Gets all handlers.

        Returns:
            (set[Handler]): set of handlers.
        """
        return cls._handlers

    @classmethod
    def get_handler(cls, handler_name: str) -> Handler:
        """
        Returns a handler with the given name.
        Args:
            handler_name (str): name of handler.

        Returns:
            (Handler): handler.
        """
        for handler in cls._handlers:
            if handler.name == handler_name:
                return handler
        msg = f"No handler with name {handler_name!r} in {cls._handlers}"
        logger.critical(msg)
        raise ItemNotFoundError(msg)

    @classmethod
    def init_handlers(cls, config: HandlersFactoryConfig) -> None:
        """Initializes handlers with the given config."""
        package_name: str = config.package_name

        for name, cfg in config.handlers.items():
            module_name: str = cfg.module_name
            handler_object: type[Handler] = import_object(cfg.type_name, module_name, package_name)
            new_handler: Handler = handler_object(cfg)
            cls._handlers.add(new_handler)
