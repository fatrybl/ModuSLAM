from src.measurement_storage.measurements.base import (
    TimeRangeMeasurement,
    WithRawElements,
)
from src.moduslam.custom_types.aliases import Matrix3x3, Matrix4x4
from src.moduslam.data_manager.batch_factory.batch import Element
from src.utils.auxiliary_dataclasses import TimeRange


class Odometry(TimeRangeMeasurement):

    def __init__(
        self,
        timestamp: int,
        time_range: TimeRange,
        transformation: Matrix4x4,
        transition_covariance: Matrix3x3,
        orientation_covariance: Matrix3x3,
    ):
        self._timestamp = timestamp
        self._time_range = time_range
        self._tf = transformation
        self._trans_covariance = transition_covariance
        self._orientation_covariance = orientation_covariance

    @property
    def timestamp(self) -> int:
        """Timestamp of the pose odometry measurement."""
        return self._timestamp

    @property
    def time_range(self) -> TimeRange:
        """Time range of the pose odometry measurement."""
        return self._time_range

    @property
    def transformation(self) -> Matrix4x4:
        """SE(3) transformation."""
        return self._tf

    @property
    def transition_covariance(self) -> Matrix3x3:
        """Noise covariance matrix of the transition [x, y, z] part."""
        return self._trans_covariance

    @property
    def orientation_covariance(self) -> Matrix3x3:
        """Noise covariance matrix of the orientation [roll, pitch, yaw] part."""
        return self._orientation_covariance


class OdometryWithElements(Odometry, WithRawElements):

    def __init__(
        self,
        timestamp: int,
        time_range: TimeRange,
        transformation: Matrix4x4,
        transition_covariance: Matrix3x3,
        orientation_covariance: Matrix3x3,
        elements: list[Element],
    ):
        super().__init__(
            timestamp, time_range, transformation, transition_covariance, orientation_covariance
        )
        self._elements = elements

    @property
    def elements(self) -> list[Element]:
        """Elements associated with the pose odometry measurement."""
        return self._elements
