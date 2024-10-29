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
    sensors = SensorsFactory.get_all_sensors()

    expected_sensor = SensorsFactory.get_sensor("test_sensor")
    assert expected_sensor.name == sensor_config.name
    assert isinstance(expected_sensor, Sensor)
    assert expected_sensor in sensors


def test_get_sensor_not_found():
    sensor_config = SensorConfig(name="test_sensor", type_name=Sensor.__name__)
    factory_config = SensorsFactoryConfig(sensors={sensor_config.name: sensor_config})

    SensorsFactory.init_sensors(factory_config)

    with pytest.raises(ItemNotFoundError):
        SensorsFactory.get_sensor("non_existing_sensor")
