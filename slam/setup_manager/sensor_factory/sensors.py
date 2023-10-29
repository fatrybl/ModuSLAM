from typing import Type

from configs.sensors.base_sensor_parameters import ParameterConfig


class Sensor:

    """Base class for any Sensor. 
    __Hash__(), __eq__() are overridden for hashability purposes.
    """

    def __init__(self, name: str, config: Type[ParameterConfig]):
        """
        Base sesnsor object.

        Args:
            name (str): sensor name
            config (Type[Parameter]): sensor parameters.
        """
        self.name = name
        self.config = config

    def __repr__(self) -> str:
        return self.name

    def __hash__(self) -> int:
        return hash((self.name, self.config))

    def __eq__(self, value: object) -> bool:
        return self.name == value.name and self.config == value.config


class Imu(Sensor):
    """Base class for any Inertial Measurement Unit."""

    def __init__(self, name: str, config: Type[ParameterConfig]):
        super().__init__(name, config)


class StereoCamera(Sensor):
    """Base class for any Stereo Camera."""

    def __init__(self, name: str, config: Type[ParameterConfig]):
        super().__init__(name, config)


class Encoder(Sensor):
    """Base class for any wheel encoder."""

    def __init__(self, name: str, config: Type[ParameterConfig]):
        super().__init__(name, config)


class Fog(Sensor):
    """Base class for any Fiber Optic Gyroscope."""

    def __init__(self, name: str, config: Type[ParameterConfig]):
        super().__init__(name, config)


class GNSS(Sensor):
    """Base class for any Global Positioning System."""

    def __init__(self, name: str, config: Type[ParameterConfig]):
        super().__init__(name, config)


class Gps(GNSS):
    """Base class for any Global Positioning System."""

    def __init__(self, name: str, config: Type[ParameterConfig]):
        super().__init__(name, config)


class VrsGps(GNSS):
    """Base class for any Virtual Reference Station."""

    def __init__(self, name: str, config: Type[ParameterConfig]):
        super().__init__(name, config)


class Altimeter(Sensor):
    """Base class for any Altimeter."""

    def __init__(self, name: str, config: Type[ParameterConfig]):
        super().__init__(name, config)


class Lidar2D(Sensor):
    """Base class for any 2D lidar."""

    def __init__(self, name: str, config: Type[ParameterConfig]):
        super().__init__(name, config)


class Lidar3D(Sensor):
    """Base class for any 3D lidar."""

    def __init__(self, name: str, config: Type[ParameterConfig]):
        super().__init__(name, config)
