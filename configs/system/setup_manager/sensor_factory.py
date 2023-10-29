from dataclasses import dataclass

from omegaconf import MISSING

from configs.sensors.base_sensor_parameters import ParameterConfig


@dataclass
class Sensor:
    """
    Configures the sensor.
    """
    name: str = MISSING
    type: str = MISSING
    config: ParameterConfig = MISSING


@dataclass
class SensorFactoryConfig:
    all_sensors: list[Sensor] = MISSING
    used_sensors: list[Sensor] = MISSING
