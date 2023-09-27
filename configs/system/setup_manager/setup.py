from dataclasses import dataclass


@dataclass
class SensorConfig:
    name: str
    type: str
    config_name: str


@dataclass
class SetupManager:
    all_sensors: list[SensorConfig]
    used_sensors: list[SensorConfig]
