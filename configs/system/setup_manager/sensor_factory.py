from dataclasses import dataclass

from omegaconf import MISSING

from configs.sensors.base_sensor_parameters import Parameter


@dataclass
class Sensor:
    """
    Configures the sensor.
    """
    name: str = MISSING
    type: str = MISSING
    config: Parameter = MISSING


@dataclass
class SensorFactory:
    all_sensors: list[Sensor] = MISSING
    used_sensors: list[Sensor] = MISSING
