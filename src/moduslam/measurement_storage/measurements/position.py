from moduslam.custom_types.aliases import Matrix3x3, Vector3
from moduslam.measurement_storage.measurements.base import Measurement


class Position(Measurement):

    def __init__(self, timestamp: int, position: Vector3, covariance: Matrix3x3):
        """
        Args:
            timestamp: measurement timestamp.

            position: X, Y, Z coordinates.

            covariance: measurement noise covariance matrix.
        """
        self._timestamp = timestamp
        self._position = position
        self._covariance = covariance

    @property
    def timestamp(self) -> int:
        """Timestamp of the position measurement."""
        return self._timestamp

    @property
    def position(self) -> Vector3:
        """X, Y, Z coordinates of the measurement."""
        return self._position

    @property
    def covariance(self) -> Matrix3x3:
        """Noise covariance matrix of the measurement."""
        return self._covariance
