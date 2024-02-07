import logging

from configs.system.setup_manager.handler_factory import HandlerFactoryConfig
from slam.frontend_manager.handlers.ABC_handler import Handler
from slam.utils.auxiliary_methods import import_object
from slam.utils.exceptions import HandlerNotFound

logger = logging.getLogger(__name__)


class HandlerFactory:
    """
    Creates handlers.
    """

    _handlers = set[Handler]()

    @classmethod
    def get_handlers(cls) -> set[Handler]:
        """
        Gets all handlers.
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
        raise HandlerNotFound(msg)

    @classmethod
    def init_handlers(cls, config: HandlerFactoryConfig) -> None:
        """
        Initializes handlers with the given config.
        """
        module_name: str = config.module_name
        package_name: str = config.package_name

        for handler_cfg in config.handlers:
            handler_object: type[Handler] = import_object(handler_cfg.type_name, module_name, package_name)
            new_handler: Handler = handler_object(handler_cfg)
            cls._handlers.add(new_handler)
