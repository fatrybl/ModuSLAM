from dataclasses import dataclass, field

from moduslam.external.handlers_factory.handlers.handler_protocol import HandlerConfig


@dataclass
class KissIcpScanMatcherConfig(HandlerConfig):
    """Configuration for the KISS ICP odometry."""

    num_channels: int = 4  # x, y, z, intensity
    max_points_per_voxel: int = 5
    voxel_size: float = 3.0
    adaptive_initial_threshold: float = 1.0
    min_range: float = 1.0
    max_range: float = 120
    deskew: bool = False
    measurement_noise_covariance: tuple[float, float, float, float, float, float] = field(
        default_factory=lambda: (1, 1, 1, 1, 1, 1),
        metadata={"help": "Measurement noise covariance [x, y, z, roll, pitch, yaw]"},
    )
