"""Tests for the SensorsFactory class."""

import pytest

from slam.setup_manager.sensors_factory.factory import SensorsFactory
from slam.setup_manager.sensors_factory.sensors import Sensor
from slam.system_configs.setup_manager.sensor_factory import SensorFactoryConfig
from slam.system_configs.setup_manager.sensors import SensorConfig
from slam.utils.exceptions import ItemNotFoundError


class TestSensorsFactory:
    def test_init_sensors(self):
        sensor_config = SensorConfig(name="test_sensor", type_name=Sensor.__name__)

        factory_config = SensorFactoryConfig(sensors={sensor_config.name: sensor_config})

        SensorsFactory.init_sensors(factory_config)

        assert any(isinstance(sensor, Sensor) for sensor in SensorsFactory.get_sensors())
        assert isinstance(SensorsFactory.get_sensor(sensor_config.name), Sensor)

    def test_get_sensor_not_found(self):
        sensor_config = SensorConfig(name="test_sensor", type_name=Sensor.__name__)

        factory_config = SensorFactoryConfig(sensors={sensor_config.name: sensor_config})

        SensorsFactory.init_sensors(factory_config)

        with pytest.raises(ItemNotFoundError):
            SensorsFactory.get_sensor("non_existing_sensor")
