from moduslam.custom_types.aliases import Matrix3x3, Matrix4x4
from moduslam.measurement_storage.measurements.base import Measurement


class Pose(Measurement):
    def __init__(
        self,
        timestamp: int,
        pose: Matrix4x4,
        position_noise_covariance: Matrix3x3,
        orientation_noise_covariance: Matrix3x3,
    ):
        self._timestamp = timestamp
        self._pose = pose
        self._position_covariance = position_noise_covariance
        self._orientation_covariance = orientation_noise_covariance

    @property
    def timestamp(self) -> int:
        """Timestamp of the pose measurement."""
        return self._timestamp

    @property
    def pose(self) -> Matrix4x4:
        """SE(3) pose."""
        return self._pose

    @property
    def position_noise_covariance(self) -> Matrix3x3:
        """Noise covariance matrix of the position [x, y, z] part."""
        return self._position_covariance

    @property
    def orientation_noise_covariance(self) -> Matrix3x3:
        """Noise covariance matrix of the orientation [roll, pitch, yaw] part."""
        return self._orientation_covariance
