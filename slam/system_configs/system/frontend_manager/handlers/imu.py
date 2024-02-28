from dataclasses import dataclass

from system_configs.system.frontend_manager.handlers.base_handler import HandlerConfig


@dataclass
class ImuPreintegratorConfig(HandlerConfig):
    """Config for Imu Preintegrator."""
