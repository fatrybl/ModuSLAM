from pathlib import Path


class Sensor:

    """Base class for any Sensor object. 
    __Hash__(), __eq__() are overridden to prevent sensors` duplicates creation.
    """

    def __init__(self, name: str, config_file: Path):
        self.name = name
        self.config_file: Path = config_file

    def __repr__(self) -> str:
        return self.name

    def __hash__(self) -> int:
        return hash((self.name, self.config_file))

    def __eq__(self, value: object) -> bool:
        return self.name == value.name and self.config_file == value.config_file


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
