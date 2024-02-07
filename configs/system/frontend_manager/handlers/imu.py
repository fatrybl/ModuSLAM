from dataclasses import dataclass

from configs.system.frontend_manager.handlers.base_handler import HandlerConfig


@dataclass
class ImuPreintegratorConfig(HandlerConfig):
    """
    Config for Imu Preintegrator.
    """
