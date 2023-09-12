from dataclasses import dataclass, field
from pathlib import Path

from slam.utils.config import Config


@dataclass
class Pose:
    position: list[float] = field(default_factory=list)
    rotation: list[float] = field(default_factory=list)


@dataclass
class ExtrinsicParameters:
    pose: Pose


@dataclass
class IntrinsicParameters:
    measurement_covariance: list[float] = field(default_factory=list)


class Sensor:
    def __init__(self, name: str, config_file: Path):
        self.name = name
        self.config = Config.from_file(config_file)

    def _set_parameters(self) -> None:
        """
        gets parameters from config file and sets the attributes
        """


class Imu(Sensor):
    def __init__(self, name: str, config_file: Path):
        super().__init__(name, config_file)


class StereoCamera(Sensor):
    def __init__(self, name: str, config_file: Path):
        super().__init__(name, config_file)


class Encoder(Sensor):
    def __init__(self, name: str, config_file: Path):
        super().__init__(name, config_file)


class Fog(Sensor):
    def __init__(self, name: str, config_file: Path):
        super().__init__(name, config_file)


class Gps(Sensor):
    def __init__(self, name: str, config_file: Path):
        super().__init__(name, config_file)


class VrsGps(Sensor):
    def __init__(self, name: str, config_file: Path):
        super().__init__(name, config_file)


class Altimeter(Sensor):
    def __init__(self, name: str, config_file: Path):
        super().__init__(name, config_file)


class Lidar(Sensor):
    def __init__(self, name: str, config_file: Path):
        super().__init__(name, config_file)


class Lidar2D(Lidar):
    def __init__(self, name: str, config_file: Path):
        super().__init__(name, config_file)


class Lidar3D(Lidar):
    def __init__(self, name: str, config_file: Path):
        super().__init__(name, config_file)
