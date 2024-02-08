from dataclasses import dataclass

from omegaconf import MISSING

from configs.system.frontend_manager.handlers.base_handler import HandlerConfig


@dataclass
class HandlerFactoryConfig:
    """
    Config for HandlerFactory.
    """

    package_name: str = MISSING
    handlers: list[HandlerConfig] = MISSING
