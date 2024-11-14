from dataclasses import dataclass

from phd.moduslam.custom_types.aliases import Matrix3x3, Vector3


@dataclass
class ImuData:
    angular_velocity: Vector3
    acceleration: Vector3


@dataclass
class ImuCovariance:
    acceleration: Matrix3x3
    angular_velocity: Matrix3x3
    accelerometer_bias: Matrix3x3
    gyroscope_bias: Matrix3x3
    integration_noise: Matrix3x3
