from dataclasses import dataclass
from pathlib import Path

from omegaconf import MISSING


@dataclass
class SensorConfig:
    """
    Configures the sensor.
    """
    name: str = MISSING
    type: str = MISSING
    config_name: str = MISSING


@dataclass
class SetupManager:
    """
    Config for SetupManager.
    """
    all_sensors: list[SensorConfig] = MISSING
    used_sensors: list[SensorConfig] = MISSING
    sensor_config_dir: Path = MISSING
