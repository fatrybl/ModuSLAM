from dataclasses import dataclass

from slam.system_configs.setup_manager.sensors import SensorConfig


@dataclass
class SensorFactoryConfig:
    """Sensor factory configuration."""

    sensors: dict[str, SensorConfig]
