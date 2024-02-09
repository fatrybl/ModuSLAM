from dataclasses import dataclass

from omegaconf import MISSING

from configs.sensors.base_sensor_parameters import ParameterConfig


@dataclass
class SensorConfig:
    """
    Configures the sensor.
    """

    name: str = MISSING
    type: str = MISSING
    config: ParameterConfig = MISSING


@dataclass
class SensorFactoryConfig:
    all_sensors: list[SensorConfig] = MISSING
    used_sensors: list[SensorConfig] = MISSING
