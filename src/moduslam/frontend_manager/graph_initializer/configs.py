from dataclasses import dataclass, field

from moduslam.custom_types.aliases import Vector3, Vector6
from moduslam.measurement_storage.measurements.imu_bias import Bias
from moduslam.measurement_storage.measurements.linear_velocity import Velocity
from moduslam.measurement_storage.measurements.pose import Pose
from moduslam.measurement_storage.measurements.position import Position


@dataclass
class EdgeConfig:
    """Base prior configuration."""

    timestamp: int
    measurement_type_name: str
    noise_covariance: tuple[float, ...]
    measurement: tuple[float, ...]


@dataclass
class PriorPosition(EdgeConfig):
    """Position configuration."""

    measurement_type_name: str = field(default=Position.__name__)
    noise_covariance: Vector3 = (1e-3, 1e-3, 1e-3)
    measurement: Vector3 = (0, 0, 0)


@dataclass
class PriorPose(EdgeConfig):
    """Pose configuration."""

    measurement_type_name: str = field(default=Pose.__name__)
    noise_covariance: Vector6 = (1e-3, 1e-3, 1e-3, 1e-3, 1e-3, 1e-3)
    measurement: Vector6 = (0, 0, 0, 0, 0, 0)


@dataclass
class PriorLinearVelocity(EdgeConfig):
    """Linear velocity configuration."""

    measurement_type_name: str = field(default=Velocity.__name__)
    noise_covariance: Vector3 = (1e-3, 1e-3, 1e-3)
    measurement: Vector3 = (0, 0, 0)


@dataclass
class PriorImuBias(EdgeConfig):
    """IMU bias configuration."""

    measurement_type_name: str = field(default=Bias.__name__)
    noise_covariance: Vector6 = (1e-3, 1e-3, 1e-3, 1e-3, 1e-3, 1e-3)
    measurement: Vector6 = (0, 0, 0, 0, 0, 0)
