from dataclasses import dataclass

from system_configs.system.frontend_manager.handlers.base_handler import HandlerConfig


@dataclass
class HandlersFactoryConfig:
    """Config for HandlerFactory."""

    package_name: str
    handlers: dict[str, HandlerConfig]
