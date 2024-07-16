from dataclasses import dataclass, field

from moduslam.system_configs.frontend_manager.handlers.base_handler import HandlerConfig


@dataclass
class FeatureDetectorConfig(HandlerConfig):
    skip_n_frames: int = 0
    noise_variance: tuple[float, float] = field(
        default_factory=lambda: (1, 1), metadata={"unit": "pixel"}
    )
