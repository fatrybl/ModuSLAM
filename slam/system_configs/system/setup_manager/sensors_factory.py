from dataclasses import dataclass


@dataclass
class SensorConfig:
    """Configures the sensor."""

    name: str
    type_name: str


@dataclass
class SensorFactoryConfig:
    """Configures the sensors factory."""

    sensors: dict[str, SensorConfig]
