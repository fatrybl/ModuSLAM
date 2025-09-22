from moduslam.custom_types.aliases import Matrix3x3, Vector3
from moduslam.data_manager.batch_factory.batch import Element
from moduslam.measurement_storage.measurements.base import WithRawElements


class PositionLandmark(WithRawElements):
    def __init__(
        self,
        timestamp: int,
        position: Vector3,
        covariance: Matrix3x3,
        descriptor: tuple[int, ...],
        element: Element,
    ):
        self._timestamp = timestamp
        self._position = position
        self._covariance = covariance
        self._descriptor = descriptor
        self._elements = [element]

    @property
    def elements(self) -> list[Element]:
        """Elements associated with the position landmark measurement."""
        return self._elements

    @property
    def timestamp(self) -> int:
        """Timestamp of the position landmark measurement."""
        return self._timestamp

    @property
    def position(self) -> Vector3:
        """X, Y, Z coordinates of the position landmark measurement."""
        return self._position

    @property
    def covariance(self) -> Matrix3x3:
        """Noise covariance matrix of the position [x, y, z] part."""
        return self._covariance

    @property
    def descriptor(self) -> tuple[int, ...]:
        """Descriptor of the position landmark."""
        return self._descriptor
