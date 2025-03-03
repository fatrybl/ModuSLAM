from src.custom_types.aliases import Matrix3x3, Matrix4x4
from src.measurement_storage.measurements.base import WithRawElements
from src.moduslam.data_manager.batch_factory.batch import Element


class PoseLandmark(WithRawElements):
    def __init__(
        self,
        timestamp: int,
        pose: Matrix4x4,
        position_covariance: Matrix3x3,
        orientation_covariance: Matrix3x3,
        descriptor: tuple[int, ...],
        element: Element,
    ):
        self._timestamp = timestamp
        self._pose = pose
        self._position_covariance = position_covariance
        self._orientation_covariance = orientation_covariance
        self._descriptor = descriptor
        self._elements = [element]

    @property
    def timestamp(self) -> int:
        """Timestamp of the pose landmark measurement."""
        return self._timestamp

    @property
    def elements(self) -> list[Element]:
        """Elements associated with the pose landmark measurement."""
        return self._elements

    @property
    def pose(self) -> Matrix4x4:
        """SE(3) pose."""
        return self._pose

    @property
    def position_covariance(self) -> Matrix3x3:
        """Noise covariance matrix of the position [x, y, z]."""
        return self._position_covariance

    @property
    def orientation_covariance(self) -> Matrix3x3:
        """Noise covariance matrix of the orientation [roll, pitch, yaw]."""
        return self._orientation_covariance

    @property
    def descriptor(self) -> tuple[int, ...]:
        """Descriptor of the landmark."""
        return self._descriptor
