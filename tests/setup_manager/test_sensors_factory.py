"""Tests for the SensorsFactory class."""

import pytest

from slam.setup_manager.sensors_factory.factory import SensorsFactory
from slam.setup_manager.sensors_factory.sensors import Sensor
from slam.system_configs.system.setup_manager.sensors import (
    SensorConfig,
    SensorFactoryConfig,
)
from slam.utils.exceptions import ItemNotFoundError


class TestSensorsFactory:
    def test_init_sensors(self):
        sensor_config = SensorConfig(name="test_sensor", type_name=Sensor.__name__)

        factory_config = SensorFactoryConfig(sensors={sensor_config.name: sensor_config})

        SensorsFactory.init_sensors(factory_config)

        assert any(isinstance(sensor, Sensor) for sensor in SensorsFactory.all_sensors())
        assert isinstance(SensorsFactory.get_sensor(sensor_config.name), Sensor)

    def test_init_sensors_empty_config(self):
        factory_config = SensorFactoryConfig(sensors={})

        with pytest.raises(ValueError):
            SensorsFactory.init_sensors(factory_config)

    def test_get_sensor_not_found(self):
        sensor_config = SensorConfig(name="test_sensor", type_name=Sensor.__name__)

        factory_config = SensorFactoryConfig(sensors={sensor_config.name: sensor_config})

        SensorsFactory.init_sensors(factory_config)

        with pytest.raises(ItemNotFoundError):
            SensorsFactory.get_sensor("non_existing_sensor")
