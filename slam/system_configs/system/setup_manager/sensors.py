from dataclasses import dataclass, field

from slam.setup_manager.sensors_factory.sensors import Lidar3D, Sensor


@dataclass
class SensorConfig:
    """Configures the sensor."""

    name: str
    type_name: str = Sensor.__name__


@dataclass
class Lidar3DConfig(SensorConfig):
    """Configures the 3D lidar sensor."""

    type_name: str = field(default=Lidar3D.__name__, metadata={"help": "Name of sensor`s type."})

    max_range: float = 100.0
    min_range: float = 0
    fov: float = field(
        default=360.0,
        metadata={"help": "Field of view in degrees."},
    )
    num_channels: int = field(
        default=4,
        metadata={"help": "Number of channels per point: x, y, z, intensity"},
    )
    tf_base_sensor: list[list[float]] = field(
        default_factory=lambda: [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]],
        metadata={"help": "Transformation matrix from sensor to base link."},
    )


@dataclass
class SensorFactoryConfig:
    """Configures the sensors factory."""

    sensors: dict[str, SensorConfig]
