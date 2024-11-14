from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from phd.moduslam.custom_types.aliases import Matrix3x3, Matrix4x4, Vector3
from phd.moduslam.data_manager.batch_factory.batch import Element
from phd.moduslam.frontend_manager.handlers.imu_data_preprocessors.objects import (
    ImuCovariance,
    ImuData,
)
from phd.moduslam.utils.auxiliary_dataclasses import TimeRange, VisualFeature


class Measurement(ABC):
    """Base absract measurement."""

    @property
    @abstractmethod
    def timestamp(self) -> int:
        """Timestamp of the measurement."""

    @property
    @abstractmethod
    def elements(self) -> list[Element]:
        """Raw elements used to form the measurement."""


M = TypeVar("M", bound=Measurement)


class VisualFeatures(Measurement):
    def __init__(self):
        raise NotImplementedError

    @property
    def elements(self) -> list[Element]:
        raise NotImplementedError

    @property
    def timestamp(self) -> int:
        raise NotImplementedError

    @property
    def features(self) -> list[VisualFeature]:
        raise NotImplementedError


class ContinuousMeasurement(Generic[M], Measurement):
    """A measurement consisting of multiple measurements.

    Consists of multiple measurements.
    """

    def __init__(self, measurements: list[M]):
        """
        Args:
            measurements: sorted by timestamp measurements (assumed to be pre-integrated).
        """

        if len(measurements) == 0:
            raise ValueError("Not enough elements to create a measurement.")

        start = min(m.timestamp for m in measurements)
        stop = max(m.timestamp for m in measurements)
        self._timestamp = stop
        self._time_range = TimeRange(start, stop)
        self._items = measurements
        self._elements = [element for m in measurements for element in m.elements]

    def __repr__(self):
        return f"num elements: {len(self._items)}"

    @property
    def timestamp(self) -> int:
        return self._timestamp

    @property
    def time_range(self) -> TimeRange:
        return self._time_range

    @property
    def items(self) -> list[M]:
        return self._items

    @property
    def elements(self) -> list[Element]:
        return self._elements


class Imu(Measurement):
    """Represents an IMU measurement."""

    def __init__(
        self, element: Element, data: ImuData, covariance: ImuCovariance, tf_base_sensor: Matrix4x4
    ):
        self._timestamp = element.timestamp
        self._acceleration = data.acceleration
        self._angular_velocity = data.angular_velocity
        self._acceleration_covariance = covariance.acceleration
        self._angular_velocity_covariance = covariance.angular_velocity
        self._integration_noise_covariance = covariance.integration_noise
        self._accelerometer_bias_covariance = covariance.accelerometer_bias
        self._gyroscope_bias_covariance = covariance.gyroscope_bias
        self._tf = tf_base_sensor
        self._elements = [element]

    @property
    def elements(self) -> list[Element]:
        """Elements associated with the IMU measurement."""
        return self._elements

    @property
    def timestamp(self) -> int:
        """Timestamp of the IMU measurement."""
        return self._timestamp

    @property
    def acceleration(self) -> Vector3:
        """Acceleration part of the IMU measurement."""
        return self._acceleration

    @property
    def angular_velocity(self) -> Vector3:
        """Angular velocity part of the IMU measurement."""
        return self._angular_velocity

    @property
    def tf_base_sensor(self) -> Matrix4x4:
        return self._tf

    @property
    def acceleration_covariance(self) -> Matrix3x3:
        """Noise covariance matrix of the acceleration part."""
        return self._acceleration_covariance

    @property
    def angular_velocity_covariance(self) -> Matrix3x3:
        """Noise covariance matrix of the angular velocity part."""
        return self._angular_velocity_covariance

    @property
    def integration_noise_covariance(self) -> Matrix3x3:
        """Noise covariance matrix of the integration process."""
        return self._integration_noise_covariance

    @property
    def accelerometer_bias_covariance(self) -> Matrix3x3:
        """Noise covariance matrix of the accelerometer bias (Random Walk process)."""
        return self._accelerometer_bias_covariance

    @property
    def gyroscope_bias_covariance(self) -> Matrix3x3:
        """Noise covariance matrix of the gyroscope bias (Random Walk process)."""
        return self._gyroscope_bias_covariance


class Gps(Measurement):

    def __init__(self, element: Element, position: Vector3, covariance: Matrix3x3):
        self._timestamp = element.timestamp
        self._position = position
        self._covariance = covariance
        self._elements = [element]

    @property
    def elements(self) -> list[Element]:
        """Elements associated with the GPS measurement."""
        return self._elements

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


class PoseOdometry(Measurement):

    def __init__(
        self,
        timestamp: int,
        time_range: TimeRange,
        pose: Matrix4x4,
        position_covariance: Matrix3x3,
        orientation_covariance: Matrix3x3,
        elements: list[Element],
    ):
        self._timestamp = timestamp
        self._time_range = time_range
        self._pose = pose
        self._position_covariance = position_covariance
        self._orientation_covariance = orientation_covariance
        self._elements = elements

    @property
    def elements(self) -> list[Element]:
        """Elements associated with the pose odometry measurement."""
        return self._elements

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


class PositionLandmark(Measurement):
    def __init__(
        self,
        timestamp: int,
        position: Vector3,
        covariance: Matrix3x3,
        descriptor: tuple[int, ...],
        elements: list[Element],
    ):
        self._timestamp = timestamp
        self._position = position
        self._covariance = covariance
        self._descriptor = descriptor
        self._elements = elements

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


class PoseLandmark(Measurement):
    def __init__(
        self,
        timestamp: int,
        pose: Matrix4x4,
        position_covariance: Matrix3x3,
        orientation_covariance: Matrix3x3,
        descriptor: tuple[int, ...],
        elements: list[Element],
    ):
        self._timestamp = timestamp
        self._pose = pose
        self._position_covariance = position_covariance
        self._orientation_covariance = orientation_covariance
        self._descriptor = descriptor
        self._elements = elements

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
        """Noise covariance matrix of the position [x, y, z] part."""
        return self._position_covariance

    @property
    def orientation_covariance(self) -> Matrix3x3:
        """Noise covariance matrix of the orientation [roll, pitch, yaw] part."""
        return self._orientation_covariance

    @property
    def descriptor(self) -> tuple[int, ...]:
        """Descriptor of the landmark."""
        return self._descriptor


class Pose(Measurement):
    def __init__(
        self,
        timestamp: int,
        pose: Matrix4x4,
        position_noise_covariance: Matrix3x3,
        orientation_noise_covariance: Matrix3x3,
        elements: list[Element],
    ):
        self._timestamp = timestamp
        self._pose = pose
        self._position_covariance = position_noise_covariance
        self._orientation_covariance = orientation_noise_covariance
        self._elements = elements

    @property
    def timestamp(self) -> int:
        """Timestamp of the pose measurement."""
        return self._timestamp

    @property
    def elements(self) -> list[Element]:
        """Elements associated with the pose measurement."""
        return self._elements

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


class LinearVelocity(Measurement):
    def __init__(
        self,
        timestamp: int,
        velocity: Vector3,
        noise_covariance: Matrix3x3,
        elements: list[Element],
    ):
        self._timestamp = timestamp
        self._velocity = velocity
        self._covariance = noise_covariance
        self._elements = elements

    @property
    def timestamp(self) -> int:
        """Timestamp of the pose measurement."""
        return self._timestamp

    @property
    def elements(self) -> list[Element]:
        """Elements associated with the pose measurement."""
        return self._elements

    @property
    def velocity(self) -> Vector3:
        """Linear velocity [Vx, Vy, Vz]."""
        return self._velocity

    @property
    def noise_covariance(self) -> Matrix3x3:
        """Noise covariance matrix."""
        return self._covariance


class ImuBias(Measurement):
    def __init__(
        self,
        timestamp: int,
        linear_acceleration_bias: Vector3,
        linear_velocity_bias: Vector3,
        linear_acceleration_noice_covariance: Matrix3x3,
        angular_velocity_noice_covariance: Matrix3x3,
        elements: list[Element],
    ):

        self._timestamp = timestamp
        self._acceleration_bias = linear_acceleration_bias
        self._linear_velocity_bias = linear_velocity_bias
        self._acceleration_noise_covariance = linear_acceleration_noice_covariance
        self._angular_velocity_noise_covariance = angular_velocity_noice_covariance
        self._elements = elements

    @property
    def timestamp(self) -> int:
        """Timestamp of the IMU bias measurement."""
        return self._timestamp

    @property
    def elements(self) -> list[Element]:
        """Elements associated with the IMU bias measurement."""
        return self._elements

    @property
    def linear_acceleration_bias(self) -> Vector3:
        """Linear acceleration bias [Bx, By, Bz]."""
        return self._acceleration_bias

    @property
    def linear_velocity_bias(self) -> Vector3:
        """Linear velocity bias [Vx, Vy, Vz]."""
        return self._linear_velocity_bias

    @property
    def linear_acceleration_noise_covariance(self) -> Matrix3x3:
        """Noise covariance matrix of the linear acceleration bias [Bx, By, Bz]."""
        return self._acceleration_noise_covariance

    @property
    def angular_velocity_noise_covariance(self) -> Matrix3x3:
        """Noise covariance matrix of the angular velocity bias [roll, pitch, yaw]."""
        return self._angular_velocity_noise_covariance
