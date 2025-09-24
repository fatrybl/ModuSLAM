"""Auxiliary functions for test data generation."""

from collections.abc import Iterable

from moduslam.sensors_factory.configs import SensorConfig
from moduslam.sensors_factory.sensors import Sensor


def generate_sensors_factory_config(sensors: Iterable[Sensor]) -> list[SensorConfig]:
    """Generates SensorsFactoryConfig from a sequence of sensors.

    Args:
        sensors: sensors to generate configurations for.
    """

    configs: list[SensorConfig] = []
    for sensor in sensors:
        sensor_cfg = SensorConfig(sensor.name, sensor.__class__.__name__)
        configs.append(sensor_cfg)

    return configs
