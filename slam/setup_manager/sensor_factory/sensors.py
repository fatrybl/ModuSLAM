from pathlib import Path


class Sensor:

    """Base class for any Sensor. 
    __Hash__(), __eq__() are overridden to prevent sensors` duplicates creation.
    """

    def __init__(self, name: str, config_file: Path):
        """_summary_

        Args:
            name (str): UNIQUE name of a sensor. Used to distinguish between different sensors.
            config_file (Path): UNIQUE configuration file of a sensor. Used to distinguish between different sensors.
        """
        self.name = name
        self.config_file: Path = config_file

    def __repr__(self) -> str:
        return self.name

    def __hash__(self) -> int:
        return hash((self.name, self.config_file))

    def __eq__(self, value: object) -> bool:
        return self.name == value.name and self.config_file == value.config_file


class Imu(Sensor):
    """Base class for any Inertial Measurement Unit."""

    def __init__(self, name: str, config_file: Path):
        super().__init__(name, config_file)


class StereoCamera(Sensor):
    """Base class for any Stereo Camera."""

    def __init__(self, name: str, config_file: Path):
        super().__init__(name, config_file)


class Encoder(Sensor):
    """Base class for any wheel encoder."""

    def __init__(self, name: str, config_file: Path):
        super().__init__(name, config_file)


class Fog(Sensor):
    """Base class for any Fiber Optic Gyroscope."""

    def __init__(self, name: str, config_file: Path):
        super().__init__(name, config_file)


class GNSS(Sensor):
    """Base class for any Global Positioning System."""

    def __init__(self, name: str, config_file: Path):
        super().__init__(name, config_file)


class Gps(GNSS):
    """Base class for any Global Positioning System."""

    def __init__(self, name: str, config_file: Path):
        super().__init__(name, config_file)


class VrsGps(GNSS):
    """Base class for any Virtual Reference Station."""

    def __init__(self, name: str, config_file: Path):
        super().__init__(name, config_file)


class Altimeter(Sensor):
    """Base class for any Altimeter."""

    def __init__(self, name: str, config_file: Path):
        super().__init__(name, config_file)


class Lidar2D(Sensor):
    """Base class for any 2D lidar."""

    def __init__(self, name: str, config_file: Path):
        super().__init__(name, config_file)


class Lidar3D(Sensor):
    """Base class for any 3D lidar."""

    def __init__(self, name: str, config_file: Path):
        super().__init__(name, config_file)
