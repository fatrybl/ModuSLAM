from dataclasses import dataclass, field

from phd.external.handlers_factory.handlers.handler_protocol import HandlerConfig


@dataclass
class KissIcpScanMatcherConfig(HandlerConfig):
    """Configuration for the KISS ICP odometry."""

    max_points_per_voxel: int = 10
    voxel_size: float = 1.5
    adaptive_initial_threshold: float = 3.0
    min_range: float = 10
    max_range: float = 100
    deskew: bool = False
    preprocess: bool = False
    measurement_noise_covariance: tuple[float, float, float, float, float, float] = field(
        default_factory=lambda: (1, 1, 1, 1, 1, 1),
        metadata={"help": "Measurement noise covariance [x, y, z, roll, pitch, yaw]"},
    )
