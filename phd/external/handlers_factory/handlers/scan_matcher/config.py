from dataclasses import dataclass, field

from phd.external.handlers_factory.handlers.handler_protocol import HandlerConfig


@dataclass
class KissIcpScanMatcherConfig(HandlerConfig):
    """Configuration for the KISS ICP odometry."""

    max_points_per_voxel: int = 20
    voxel_size: float = 1.0
    adaptive_initial_threshold: float = 2.0
    min_range: float = 5
    max_range: float = 120
    deskew: bool = False
    measurement_noise_covariance: tuple[float, float, float, float, float, float] = field(
        default_factory=lambda: (1, 1, 1, 1, 1, 1),
        metadata={"help": "Measurement noise covariance [x, y, z, roll, pitch, yaw]"},
    )
