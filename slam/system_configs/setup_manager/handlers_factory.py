from dataclasses import dataclass

from slam.system_configs.frontend_manager.handlers.base_handler import HandlerConfig


@dataclass
class HandlersFactoryConfig:
    """Base handlers factory configuration."""

    package_name: str
    handlers: dict[str, HandlerConfig]
