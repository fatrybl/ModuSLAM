from dataclasses import dataclass

from moduslam.system_configs.frontend_manager.handlers.base_handler import HandlerConfig


@dataclass
class HandlersFactoryConfig:
    """Base handlers factory configuration."""

    package_name: str
    handlers: dict[str, HandlerConfig]
