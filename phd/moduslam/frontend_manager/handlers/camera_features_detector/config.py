"""Configuration for camera features detector."""

from dataclasses import dataclass, field

from phd.moduslam.frontend_manager.handlers.handler_protocol import HandlerConfig


@dataclass
class FeatureDetectorConfig(HandlerConfig):
    skip_n_frames: int = 0
    noise_variance: tuple[float, float] = field(
        default_factory=lambda: (2.0, 2.0), metadata={"unit": "pixel"}
    )
