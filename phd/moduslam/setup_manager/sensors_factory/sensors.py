"""The module contains the base classes for sensors.

Use them to create new sensors if needed.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from moduslam.system_configs.setup_manager.sensors import (
        ImuConfig,
        Lidar3DConfig,
        SensorConfig,
        StereoCameraConfig,
    )


class Sensor:
    """Base class for any Sensor.

    __Hash__(), __eq__() are overridden for hash ability purposes.
    """

    def __init__(self, config: SensorConfig):
        """Base sensor object.

        Args:
            config (SensorConfig): sensor parameters.
        """
        self._name = config.name

    def __repr__(self) -> str:
        return self.name

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, value: Any) -> bool:
        return self.name == value.name

    @property
    def name(self) -> str:
        """Name of the sensor."""
        return self._name


class Imu(Sensor):
    """Base class for any Inertial Measurement Unit."""

    def __init__(self, config: ImuConfig):
        """
        Args:
            config: Sensor configuration.
        """
        super().__init__(config)
        self._tf_base_sensor = config.tf_base_sensor
        self._accelerometer_noise_covariance = config.accelerometer_noise_covariance
        self._gyroscope_noise_covariance = config.gyroscope_noise_covariance
        self._integration_noise_covariance = config.integration_noise_covariance
        self._accelerometer_bias_noise_covariance = config.accelerometer_bias_noise_covariance
        self._gyroscope_bias_noise_covariance = config.gyroscope_bias_noise_covariance

    @property
    def tf_base_sensor(self) -> list[list[float]]:
        """Base -> sensor transformation SE(3)."""
        return self._tf_base_sensor

    @property
    def accelerometer_noise_covariance(self) -> list[list[float]]:
        """Accelerometer noise covariance diagonal matrix [3, 3]."""
        return self._accelerometer_noise_covariance

    @property
    def gyroscope_noise_covariance(self) -> list[list[float]]:
        """Gyroscope noise covariance diagonal matrix [3, 3]."""
        return self._gyroscope_noise_covariance

    @property
    def integration_noise_covariance(self) -> list[list[float]]:
        """Integration noise covariance diagonal matrix [3, 3]."""
        return self._integration_noise_covariance

    @property
    def accelerometer_bias_noise_covariance(self) -> list[list[float]]:
        """Accelerometer bias noise covariance diagonal matrix [3, 3]."""
        return self._accelerometer_bias_noise_covariance

    @property
    def gyroscope_bias_noise_covariance(self) -> list[list[float]]:
        """Gyroscope bias noise covariance diagonal matrix [3, 3]."""
        return self._gyroscope_bias_noise_covariance


class StereoCamera(Sensor):
    """Base class for any Stereo Camera."""

    def __init__(self, config: StereoCameraConfig):
        """
        Args:
            config: Sensor configuration.
        """
        super().__init__(config)
        self._config = config
        self._tf_base_sensor = config.tf_base_sensor

    @property
    def calibrations(self) -> StereoCameraConfig:
        """Camera calibration parameters."""
        return self._config

    @property
    def tf_base_sensor(self) -> list[list[float]]:
        """Base -> sensor transformation SE(3)."""
        return self._tf_base_sensor


class Encoder(Sensor):
    """Base class for any wheel encoder."""

    def __init__(self, config: SensorConfig):
        """
        Args:
            config: Sensor configuration.
        """
        super().__init__(config)


class Fog(Sensor):
    """Base class for any Fiber Optic Gyroscope."""

    def __init__(self, config: SensorConfig):
        """
        Args:
            config: Sensor configuration.
        """
        super().__init__(config)


class GNSS(Sensor):
    """Base class for any Global Positioning System."""

    def __init__(self, config: SensorConfig):
        """
        Args:
            config: Sensor configuration.
        """
        super().__init__(config)


class Gps(GNSS):
    """Base class for any Global Positioning System."""

    def __init__(self, config: SensorConfig):
        """
        Args:
            config: Sensor configuration.
        """
        super().__init__(config)


class VrsGps(GNSS):
    """Base class for any Virtual Reference Station."""

    def __init__(self, config: SensorConfig):
        """
        Args:
            config: Sensor configuration.
        """
        super().__init__(config)


class Altimeter(Sensor):
    """Base class for any Altimeter."""

    def __init__(self, config: SensorConfig):
        """
        Args:
            config: Sensor configuration.
        """
        super().__init__(config)


class Lidar2D(Sensor):
    """Base class for any 2D lidar."""

    def __init__(self, config: SensorConfig):
        """
        Args:
            config: Sensor configuration.
        """
        super().__init__(config)


class Lidar3D(Sensor):
    """Base class for 3D lidar."""

    def __init__(self, config: Lidar3DConfig):
        """
        Args:
            config: Sensor configuration.
        """
        super().__init__(config)
        self._tf_base_sensor = config.tf_base_sensor

    @property
    def tf_base_sensor(self) -> list[list[float]]:
        """Base -> sensor transformation SE(3)."""
        return self._tf_base_sensor
