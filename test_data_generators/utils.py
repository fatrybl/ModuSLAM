"""Auxiliary functions for test data generation."""

from collections.abc import Sequence

from moduslam.setup_manager.sensors_factory.sensors import Sensor
from moduslam.system_configs.setup_manager.sensor_factory import SensorsFactoryConfig
from moduslam.system_configs.setup_manager.sensors import SensorConfig


def generate_sensors_factory_config(sensors: Sequence[Sensor]) -> SensorsFactoryConfig:
    """Generates SensorsFactoryConfig from a sequence of sensors.

    Args:
        sensors: sensors to generate configurations for.
    """

    configs: dict[str, SensorConfig] = {}
    for sensor in sensors:
        sensor_cfg = SensorConfig(
            name=sensor.name,
            type_name=sensor.__class__.__name__,
        )
        configs[sensor.name] = sensor_cfg

    return SensorsFactoryConfig(configs)
