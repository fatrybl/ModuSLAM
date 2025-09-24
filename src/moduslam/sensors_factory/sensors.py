"""Different sensors are stored here.

TODO: maybe avoid redefining __hash__ and __eq__ methods for base sensor?
    this demands huge tests refactoring for data readers.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from moduslam.custom_types.aliases import Matrix3x3, Matrix4x4
from moduslam.utils.auxiliary_methods import matrix3x3_list_to_tuple as tuple3x3
from moduslam.utils.auxiliary_methods import matrix4x4_list_to_tuple as tuple4x4

if TYPE_CHECKING:
    from moduslam.sensors_factory.configs import (
        ImuConfig,
        Lidar3DConfig,
        MonocularCameraConfig,
        SensorConfig,
        StereoCameraConfig,
        UltraWideBandConfig,
        VrsGpsConfig,
    )


class Sensor:
    """Base sensor."""

    def __init__(self, name: str):
        """
        Args:
            name: unique sensor name.
        """
        self._name = name

    def __eq__(self, other) -> bool:
        if type(other) is not type(self):
            return NotImplemented
        return vars(self) == vars(other)

    def __hash__(self) -> int:
        return hash((self._name,))

    def __repr__(self) -> str:
        return self._name

    @property
    def name(self) -> str:
        """Name of the sensor."""
        return self._name


class Imu(Sensor):
    """Base class for any Inertial Measurement Unit."""

    def __init__(self, config: ImuConfig):
        """
        Args:
            config: sensor configuration.
        """
        super().__init__(config.name)
        self._tf_base_sensor = tuple4x4(config.tf_base_sensor)
        self._accel_noise_covariance = tuple3x3(config.accelerometer_noise_covariance)
        self._gyro_noise_covariance = tuple3x3(config.gyroscope_noise_covariance)
        self._integration_noise_covariance = tuple3x3(config.integration_noise_covariance)
        self._accel_bias_noise_covariance = tuple3x3(config.accelerometer_bias_noise_covariance)
        self._gyro_bias_noise_covariance = tuple3x3(config.gyroscope_bias_noise_covariance)

    @property
    def tf_base_sensor(self) -> Matrix4x4:
        """Base -> sensor transformation SE(3)."""
        return self._tf_base_sensor

    @property
    def accelerometer_noise_covariance(self) -> Matrix3x3:
        """Accelerometer noise covariance diagonal matrix [3, 3]."""
        return self._accel_noise_covariance

    @property
    def gyroscope_noise_covariance(self) -> Matrix3x3:
        """Gyroscope noise covariance diagonal matrix [3, 3]."""
        return self._gyro_noise_covariance

    @property
    def integration_noise_covariance(self) -> Matrix3x3:
        """Integration noise covariance diagonal matrix [3, 3]."""
        return self._integration_noise_covariance

    @property
    def accelerometer_bias_noise_covariance(self) -> Matrix3x3:
        """Accelerometer bias noise covariance diagonal matrix [3, 3]."""
        return self._accel_bias_noise_covariance

    @property
    def gyroscope_bias_noise_covariance(self) -> Matrix3x3:
        """Gyroscope bias noise covariance diagonal matrix [3, 3]."""
        return self._gyro_bias_noise_covariance


class MonocularCamera(Sensor):
    """Base class for any Monocular Camera."""

    def __init__(self, config: MonocularCameraConfig):
        """
        Args:
            config: Sensor configuration.
        """
        super().__init__(config.name)
        self._config = config
        self._tf_base_sensor = tuple4x4(config.tf_base_sensor)

    @property
    def tf_base_sensor(self) -> Matrix4x4:
        """Base -> sensor transformation SE(3)."""
        return self._tf_base_sensor

    @property
    def calibrations(self) -> MonocularCameraConfig:
        """Camera calibration parameters."""
        return self._config


class StereoCamera(Sensor):
    """Base class for any Stereo Camera."""

    def __init__(self, config: StereoCameraConfig):
        """
        Args:
            config: Sensor configuration.
        """
        super().__init__(config.name)
        self._config = config
        self._tf_base_sensor = tuple4x4(config.tf_base_sensor)

    @property
    def calibrations(self) -> StereoCameraConfig:
        """Camera calibration parameters."""
        return self._config

    @property
    def tf_base_sensor(self) -> Matrix4x4:
        """Base -> sensor transformation SE(3)."""
        return self._tf_base_sensor


class Encoder(Sensor):
    """Base class for any wheel encoder."""

    def __init__(self, config: SensorConfig):
        """
        Args:
            config: sensor configuration.
        """
        super().__init__(config.name)


class Fog(Sensor):
    """Base class for any Fiber Optic Gyroscope."""

    def __init__(self, config: SensorConfig):
        """
        Args:
            config: sensor configuration.
        """
        super().__init__(config.name)


class GNSS(Sensor):
    """Base class for any Global Positioning System."""

    def __init__(self, config: SensorConfig):
        """
        Args:
            config: sensor configuration.
        """
        super().__init__(config.name)


class Gps(GNSS):
    """Base class for any Global Positioning System."""

    def __init__(self, config: SensorConfig):
        """
        Args:
            config: sensor configuration.
        """
        super().__init__(config)


class VrsGps(GNSS):
    """Base class for any Virtual Reference Station."""

    def __init__(self, config: VrsGpsConfig):
        """
        Args:
            config: sensor configuration.
        """
        super().__init__(config)
        self._tf_base_sensor = tuple4x4(config.tf_base_sensor)

    @property
    def tf_base_sensor(self) -> Matrix4x4:
        """Base -> sensor transformation SE(3)."""
        return self._tf_base_sensor


class Altimeter(Sensor):
    """Base class for any Altimeter."""

    def __init__(self, config: SensorConfig):
        """
        Args:
            config: sensor configuration.
        """
        super().__init__(config.name)


class Lidar2D(Sensor):
    """Base class for any 2D lidar."""

    def __init__(self, config: SensorConfig):
        """
        Args:
            config: sensor configuration.
        """
        super().__init__(config.name)


class Lidar3D(Sensor):
    """Base class for 3D lidar."""

    def __init__(self, config: Lidar3DConfig):
        """
        Args:
            config: sensor configuration.
        """
        super().__init__(config.name)
        self._tf_base_sensor = tuple4x4(config.tf_base_sensor)

    @property
    def tf_base_sensor(self) -> Matrix4x4:
        """Base -> sensor transformation SE(3)."""
        return self._tf_base_sensor


class UltraWideBand(Sensor):
    """Base class for any Ultra Wide Band."""

    def __init__(self, config: UltraWideBandConfig):
        """
        Args:
            config: sensor configuration.
        """
        super().__init__(config.name)
