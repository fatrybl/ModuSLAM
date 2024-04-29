from dataclasses import dataclass

from slam.system_configs.frontend_manager.handlers.base_handler import HandlerConfig


@dataclass
class ImuPreintegratorConfig(HandlerConfig):
    """IMU preintegrator configuration."""
