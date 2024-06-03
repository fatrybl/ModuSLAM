from dataclasses import dataclass

from moduslam.system_configs.frontend_manager.handlers.base_handler import HandlerConfig


@dataclass
class VisualOdometryConfig(HandlerConfig):
    skip_n_frames: int = 0
    noise_variance: tuple[float, float, float, float, float, float] = (1, 1, 1, 1, 1, 1)
