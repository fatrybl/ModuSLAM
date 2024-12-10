from phd.measurement_storage.measurements.base import (
    TimeRangeMeasurement,
    WithRawElements,
)
from phd.moduslam.custom_types.aliases import Matrix3x3, Matrix4x4
from phd.moduslam.data_manager.batch_factory.batch import Element
from phd.moduslam.utils.auxiliary_dataclasses import TimeRange


class Odometry(TimeRangeMeasurement):

    def __init__(
        self,
        timestamp: int,
        time_range: TimeRange,
        pose: Matrix4x4,
        position_covariance: Matrix3x3,
        orientation_covariance: Matrix3x3,
    ):
        self._timestamp = timestamp
        self._time_range = time_range
        self._pose = pose
        self._position_covariance = position_covariance
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
    def pose(self) -> Matrix4x4:
        """SE(3) pose."""
        return self._pose

    @property
    def position_covariance(self) -> Matrix3x3:
        """Noise covariance matrix of the position [x, y, z] part."""
        return self._position_covariance

    @property
    def orientation_covariance(self) -> Matrix3x3:
        """Noise covariance matrix of the orientation [roll, pitch, yaw] part."""
        return self._orientation_covariance


class OdometryWithElements(Odometry, WithRawElements):

    def __init__(
        self,
        timestamp: int,
        time_range: TimeRange,
        pose: Matrix4x4,
        position_covariance: Matrix3x3,
        orientation_covariance: Matrix3x3,
        elements: list[Element],
    ):
        super().__init__(timestamp, time_range, pose, position_covariance, orientation_covariance)
        self._elements = elements

    @property
    def elements(self) -> list[Element]:
        """Elements associated with the pose odometry measurement."""
        return self._elements
