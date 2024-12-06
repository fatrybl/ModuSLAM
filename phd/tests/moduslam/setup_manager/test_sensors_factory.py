"""Tests for the SensorsFactory class."""

import pytest

from phd.moduslam.setup_manager.sensors_factory.factory import SensorsFactory
from phd.moduslam.setup_manager.sensors_factory.sensors import Sensor
from phd.moduslam.setup_manager.sensors_factory.sensors_configs import SensorConfig
from phd.moduslam.utils.exceptions import ItemNotExistsError


def test_init_sensors():
    sensor_config = SensorConfig(name="test_sensor", type_name=Sensor.__name__)

    SensorsFactory.init_sensors({"test_sensor": sensor_config})

    sensors = SensorsFactory.get_all_sensors()
    expected_sensor = SensorsFactory.get_sensor("test_sensor")

    assert expected_sensor.name == sensor_config.name
    assert isinstance(expected_sensor, Sensor)
    assert expected_sensor in sensors


def test_init_sensors_names_mismatch():
    sensor_config = SensorConfig(name="sensor_name_A", type_name=Sensor.__name__)

    with pytest.raises(ValueError, match="Sensor`s name does not match the name in the config."):
        SensorsFactory.init_sensors({"sensor_name_B": sensor_config})


def test_get_sensor_not_found():
    sensor_config = SensorConfig(name="test_sensor", type_name=Sensor.__name__)

    SensorsFactory.init_sensors({"test_sensor": sensor_config})

    with pytest.raises(ItemNotExistsError):
        SensorsFactory.get_sensor("non_existing_sensor")
