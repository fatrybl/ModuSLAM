"""Configuration for camera features detector."""

from dataclasses import dataclass, field

from src.external.handlers_factory.handlers.handler_protocol import HandlerConfig


@dataclass
class VisualOdometryConfig(HandlerConfig):
    skip_n_frames: int = 0
    measurement_noise_covariance: tuple[float, float, float, float, float, float] = field(
        default_factory=lambda: (1, 1, 1, 1, 1, 1),
        metadata={"help": "Measurement noise covariance [x, y, z, roll, pitch, yaw]"},
    )
