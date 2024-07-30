"""Tests for the SensorsFactory class."""

import pytest

from moduslam.setup_manager.sensors_factory.factory import SensorsFactory
from moduslam.setup_manager.sensors_factory.sensors import Sensor
from moduslam.system_configs.setup_manager.sensor_factory import SensorsFactoryConfig
from moduslam.system_configs.setup_manager.sensors import SensorConfig
from moduslam.utils.exceptions import ItemNotFoundError


def test_init_sensors():
    sensor_config = SensorConfig(name="test_sensor", type_name=Sensor.__name__)

    factory_config = SensorsFactoryConfig(sensors={sensor_config.name: sensor_config})

    SensorsFactory.init_sensors(factory_config)

    assert any(isinstance(sensor, Sensor) for sensor in SensorsFactory.get_all_sensors())
    assert isinstance(SensorsFactory.get_sensor(sensor_config.name), Sensor)


def test_get_sensor_not_found():
    sensor_config = SensorConfig(name="test_sensor", type_name=Sensor.__name__)

    factory_config = SensorsFactoryConfig(sensors={sensor_config.name: sensor_config})

    SensorsFactory.init_sensors(factory_config)

    with pytest.raises(ItemNotFoundError):
        SensorsFactory.get_sensor("non_existing_sensor")
