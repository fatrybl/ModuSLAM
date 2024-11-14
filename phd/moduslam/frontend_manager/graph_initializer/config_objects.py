from dataclasses import dataclass, field

from phd.moduslam.custom_types.aliases import Vector3, Vector6
from phd.moduslam.frontend_manager.main_graph.vertices.custom import (
    ImuBias,
    LinearVelocity,
)
from phd.moduslam.frontend_manager.main_graph.vertices.custom import Pose as PoseVertex


@dataclass
class EdgeConfig:
    """Base prior configuration."""

    timestamp: int
    vertex_type_name: str
    noise_covariance: tuple[float, ...]
    measurement: tuple[float, ...]


@dataclass
class InitializerConfig:
    """Base graph initializer configuration."""

    priors: dict[str, EdgeConfig] = field(default_factory=dict)


@dataclass
class PriorPose(EdgeConfig):
    """Pose configuration."""

    vertex_type_name: str = field(default=PoseVertex.__name__)
    noise_covariance: Vector6 = (1e-5, 1e-5, 1e-5, 1e-5, 1e-5, 1e-5)
    measurement: Vector6 = (0, 0, 0, 0, 0, 0)


@dataclass
class PriorLinearVelocity(EdgeConfig):
    """Linear velocity configuration."""

    vertex_type_name: str = field(default=LinearVelocity.__name__)
    noise_covariance: Vector3 = (1e-5, 1e-5, 1e-5)
    measurement: Vector3 = (0, 0, 0)


@dataclass
class PriorImuBias(EdgeConfig):
    """IMU bias configuration."""

    vertex_type_name: str = field(default=ImuBias.__name__)
    noise_covariance: Vector6 = (1e-5, 1e-5, 1e-5, 1e-5, 1e-5, 1e-5)
    measurement: Vector6 = (0, 0, 0, 0, 0, 0)
