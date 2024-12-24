from dataclasses import dataclass
from typing import TypeVar

from phd.measurement_storage.measurements.base import Measurement
from phd.measurement_storage.measurements.continuous import ContinuousMeasurement
from phd.moduslam.custom_types.aliases import Matrix3x3, Matrix4x4, Vector3
from phd.utils.auxiliary_dataclasses import TimeRange


@dataclass
class ImuData:
    angular_velocity: Vector3
    acceleration: Vector3


@dataclass
class ImuCovariance:
    acceleration: Matrix3x3
    angular_velocity: Matrix3x3
    accelerometer_bias: Matrix3x3
    gyroscope_bias: Matrix3x3
    integration_noise: Matrix3x3


class Imu(Measurement):
    """Represents an IMU measurement."""

    def __init__(self, timestamp: int, data: ImuData):
        """
        Args:
            timestamp: timestamp of the measurement.
        """
        self._timestamp = timestamp
        self._data = data

    @property
    def timestamp(self) -> int:
        """Timestamp of the IMU measurement."""
        return self._timestamp

    @property
    def linear_acceleration(self) -> Vector3:
        """Acceleration part of the IMU measurement."""
        return self._data.acceleration

    @property
    def angular_velocity(self) -> Vector3:
        """Angular velocity part of the IMU measurement."""
        return self._data.angular_velocity


class ProcessedImu(Imu):
    """An IMU measurement processed by handler."""

    def __init__(
        self, timestamp: int, data: ImuData, covariance: ImuCovariance, tf_base_sensor: Matrix4x4
    ):
        """
        Args:
            data: IMU data.

            covariance: IMU covariance.

            tf_base_sensor: transformation from base to IMU sensor.
        """
        super().__init__(timestamp, data)
        self._acceleration_covariance = covariance.acceleration
        self._angular_velocity_covariance = covariance.angular_velocity
        self._integration_noise_covariance = covariance.integration_noise
        self._accelerometer_bias_covariance = covariance.accelerometer_bias
        self._gyroscope_bias_covariance = covariance.gyroscope_bias
        self._tf = tf_base_sensor

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


I = TypeVar("I", bound=Imu)


class ContinuousImu(ContinuousMeasurement[I]):
    """A continuous measurement with multiple IMU measurements."""

    def __init__(self, measurements: list[I], start: int, stop: int):
        """
        Args:
            measurements: sorted by timestamp IMU measurements.

            start: left timestamp limit.

            stop: right timestamp limit.

        Raises:
            ValueError: if the first measurement's timestamp is less than start.

        TODO: change list to tuple for better type checking ?
        """
        if measurements[0].timestamp < start:
            raise ValueError("Start timestamp is less than the first measurement's timestamp.")

        super().__init__(measurements)

        self._timestamp = stop
        self._time_range = TimeRange(start, stop)

    def __repr__(self):
        return f"Continuous IMU with: {len(self._items)} items."
