"""The module contains the base classes for sensors.

Use them to create new sensors if needed.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

from slam.utils.numpy_types import Matrix4x4

if TYPE_CHECKING:
    from slam.system_configs.setup_manager.sensors import Lidar3DConfig, SensorConfig


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

    def __init__(self, config: SensorConfig):
        """
        Args:
            config: Sensor configuration.
        """
        super().__init__(config)


class StereoCamera(Sensor):
    """Base class for any Stereo Camera."""

    def __init__(self, config: SensorConfig):
        """
        Args:
            config: Sensor configuration.
        """
        super().__init__(config)


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
        self._tf_base_sensor: Matrix4x4 = (
            np.eye(4)
            if config.tf_base_sensor is None
            else np.array(config.tf_base_sensor, dtype=np.float32)
        )

    @property
    def tf_base_sensor(self) -> Matrix4x4:
        """Base -> sensor transformation SE(3)."""
        return self._tf_base_sensor
