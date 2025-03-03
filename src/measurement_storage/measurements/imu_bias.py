from src.custom_types.aliases import Matrix3x3, Vector3
from src.measurement_storage.measurements.base import Measurement


class Bias(Measurement):
    def __init__(
        self,
        timestamp: int,
        linear_acceleration_bias: Vector3,
        linear_velocity_bias: Vector3,
        linear_acceleration_noice_covariance: Matrix3x3,
        angular_velocity_noice_covariance: Matrix3x3,
    ):

        self._timestamp = timestamp
        self._acceleration_bias = linear_acceleration_bias
        self._linear_velocity_bias = linear_velocity_bias
        self._acceleration_noise_covariance = linear_acceleration_noice_covariance
        self._angular_velocity_noise_covariance = angular_velocity_noice_covariance

    @property
    def timestamp(self) -> int:
        """Timestamp of the IMU bias measurement."""
        return self._timestamp

    @property
    def linear_acceleration_bias(self) -> Vector3:
        """Linear acceleration bias [Bx, By, Bz]."""
        return self._acceleration_bias

    @property
    def angular_velocity_bias(self) -> Vector3:
        """Angular velocity bias [Wx, Wy, Wz]."""
        return self._linear_velocity_bias

    @property
    def linear_acceleration_noise_covariance(self) -> Matrix3x3:
        """Noise covariance matrix of the linear acceleration bias [Bx, By, Bz]."""
        return self._acceleration_noise_covariance

    @property
    def angular_velocity_noise_covariance(self) -> Matrix3x3:
        """Noise covariance matrix of the angular velocity bias [roll, pitch, yaw]."""
        return self._angular_velocity_noise_covariance
