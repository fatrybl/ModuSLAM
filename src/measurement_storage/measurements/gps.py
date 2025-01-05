from src.measurement_storage.measurements.base import Measurement
from src.moduslam.custom_types.aliases import Matrix3x3, Vector3


class Gps(Measurement):

    def __init__(self, timestamp: int, position: Vector3, covariance: Matrix3x3):
        self._timestamp = timestamp
        self._position = position
        self._covariance = covariance

    @property
    def timestamp(self) -> int:
        """Timestamp of the GPS measurement."""
        return self._timestamp

    @property
    def position(self) -> Vector3:
        """X, Y, Z coordinates of the GPS measurement."""
        return self._position

    @property
    def covariance(self) -> Matrix3x3:
        """Noise covariance matrix of the GPS measurement."""
        return self._covariance
