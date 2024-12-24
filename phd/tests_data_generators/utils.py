"""Auxiliary functions for test data generation."""

from collections.abc import Sequence

from phd.moduslam.sensors_factory.configs import SensorConfig
from phd.moduslam.sensors_factory.sensors import Sensor


def generate_sensors_factory_config(sensors: Sequence[Sensor]) -> dict[str, SensorConfig]:
    """Generates SensorsFactoryConfig from a sequence of sensors.

    Args:
        sensors: sensors to generate configurations for.
    """

    configs: dict[str, SensorConfig] = {}
    for sensor in sensors:
        sensor_cfg = SensorConfig(sensor.name, sensor.__class__.__name__)
        configs[sensor.name] = sensor_cfg

    return configs
