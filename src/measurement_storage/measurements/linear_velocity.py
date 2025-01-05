from src.measurement_storage.measurements.base import Measurement
from src.moduslam.custom_types.aliases import Matrix3x3, Vector3


class Velocity(Measurement):
    def __init__(self, timestamp: int, velocity: Vector3, noise_covariance: Matrix3x3):
        self._timestamp = timestamp
        self._velocity = velocity
        self._covariance = noise_covariance

    @property
    def timestamp(self) -> int:
        """Timestamp of the pose measurement."""
        return self._timestamp

    @property
    def velocity(self) -> Vector3:
        """Linear velocity [Vx, Vy, Vz]."""
        return self._velocity

    @property
    def noise_covariance(self) -> Matrix3x3:
        """Noise covariance matrix."""
        return self._covariance
