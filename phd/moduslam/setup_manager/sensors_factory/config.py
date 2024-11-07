from dataclasses import dataclass

from phd.moduslam.setup_manager.sensors_factory.sensors_configs import SensorConfig


@dataclass
class SensorsFactoryConfig:
    """Sensor factory configuration."""

    sensors: dict[str, SensorConfig]
