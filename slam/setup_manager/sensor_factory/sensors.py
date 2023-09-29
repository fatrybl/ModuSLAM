from pathlib import Path

from slam.utils.config import Config


class Sensor:
    def __init__(self, name: str, config_file: Path):
        self.name = name
        self.config = Config.from_file(config_file)

    def __repr__(self) -> str:
        return self.name


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


class Lidar2D(Sensor):
    def __init__(self, name: str, config_file: Path):
        super().__init__(name, config_file)


class Lidar3D(Sensor):
    def __init__(self, name: str, config_file: Path):
        super().__init__(name, config_file)
