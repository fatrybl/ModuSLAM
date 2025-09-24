"""Tests for the SensorsFactory class."""

import pytest

from moduslam.sensors_factory.configs import SensorConfig
from moduslam.sensors_factory.factory import SensorsFactory
from moduslam.sensors_factory.sensors import Sensor
from moduslam.utils.exceptions import ItemNotExistsError


def test_init_sensors():
    config = SensorConfig(name="test_sensor")

    SensorsFactory.init_sensors([config])

    sensors = SensorsFactory.get_sensors()
    expected_sensor = SensorsFactory.get_sensor("test_sensor")

    assert expected_sensor.name == config.name
    assert isinstance(expected_sensor, Sensor)
    assert expected_sensor in sensors


def test_get_sensor_not_found():
    config = SensorConfig(name="test_sensor")

    SensorsFactory.init_sensors([config])

    with pytest.raises(ItemNotExistsError):
        SensorsFactory.get_sensor("non_existing_sensor")
