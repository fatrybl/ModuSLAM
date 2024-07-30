from dataclasses import dataclass

from moduslam.system_configs.setup_manager.sensors import SensorConfig


@dataclass
class SensorsFactoryConfig:
    """Sensor factory configuration."""

    sensors: dict[str, SensorConfig]
