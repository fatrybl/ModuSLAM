"""
Tests description:

1) Create a dataset for a DataReader.
2) Initialize config files for DataReader
3) Initialize DataReader with config files.
4) Test methods:
    4.1) get_element()
    4.2) get_element(element[Element])
    4.3) get_element(sensor[Sensor])
    4.4) get_element(sensor[Sensor], timestamp[int])
"""

import pytest
from PIL.Image import Image
from pytest import mark

from configs.sensors.base_sensor_parameters import ParameterConfig
from configs.system.setup_manager.sensors_factory import (
    SensorConfig,
    SensorFactoryConfig,
)
from slam.data_manager.factory.readers.element_factory import Element
from slam.data_manager.factory.readers.kaist.kaist_reader import KaistReader
from slam.setup_manager.sensors_factory.factory import SensorFactory
from slam.setup_manager.sensors_factory.sensors import Sensor
from tests.data_manager.auxiliary_utils.kaist_data_factory import (
    DataFactory,
    SensorElementPair,
)
from tests.data_manager.factory.readers.kaist.api.one_element_dataset.data import (
    elements,
    sensor_element_pairs,
)


class TestGetElement:
    """
    KaistReader object is used as a fixture with scope "class" to be created once.
    This prevents the creation of KaistReader objects every time the test is called with new parameters
    ==> prevents resetig of iterators for get_element() method.
    """

    @mark.parametrize("reference_element", (elements))
    def test_get_element_1(
        self,
        data_reader: KaistReader,
        reference_element: Element,
    ):
        sensor: Sensor = reference_element.measurement.sensor

        sensor_cfg: SensorConfig = SensorConfig(
            name=sensor.name, type=sensor.__class__.__name__, config=ParameterConfig()
        )
        cfg: SensorFactoryConfig = SensorFactoryConfig()
        cfg.used_sensors = [sensor_cfg]
        cfg.all_sensors = [sensor_cfg]

        SensorFactory.init_sensors(cfg)

        element: Element | None = data_reader.get_element()
        if element is None:
            pytest.fail("Element is None but should be of type Element")

        if isinstance(element.measurement.values[0], Image):
            assert DataFactory.equal_images(element, reference_element) is True
        else:
            assert element.measurement.values == reference_element.measurement.values

        assert element.timestamp == reference_element.timestamp
        assert element.location == reference_element.location
        assert element.measurement.sensor == reference_element.measurement.sensor

    @mark.parametrize("reference_element", (elements))
    def test_get_element_2(
        self,
        data_reader: KaistReader,
        reference_element: Element,
    ):
        sensor: Sensor = reference_element.measurement.sensor

        sensor_cfg: SensorConfig = SensorConfig(
            name=sensor.name, type=sensor.__class__.__name__, config=ParameterConfig()
        )
        cfg: SensorFactoryConfig = SensorFactoryConfig()
        cfg.used_sensors = [sensor_cfg]
        cfg.all_sensors = [sensor_cfg]

        SensorFactory.init_sensors(cfg)

        element: Element = data_reader.get_element(reference_element)

        if isinstance(element.measurement.values[0], Image):
            assert DataFactory.equal_images(element, reference_element) is True
        else:
            assert element.measurement.values == reference_element.measurement.values

        assert element.timestamp == reference_element.timestamp
        assert element.location == reference_element.location
        assert element.measurement.sensor == reference_element.measurement.sensor


class TestGetElementOfSensor:
    """
    KaistReader object is used as a fixture with scope "class" to be created once.
    This prevents the creation of KaistReader objects every time the test is called with new parameters
    ==> prevents resetig of iterators for get_element() method.
    """

    @mark.parametrize("sensor_element_pair", (sensor_element_pairs))
    def test_get_element_3(
        self,
        data_reader: KaistReader,
        sensor_element_pair: SensorElementPair,
    ):
        sensor: Sensor = sensor_element_pair.sensor

        sensor_cfg: SensorConfig = SensorConfig(
            name=sensor.name, type=sensor.__class__.__name__, config=ParameterConfig()
        )
        cfg: SensorFactoryConfig = SensorFactoryConfig()
        cfg.used_sensors = [sensor_cfg]
        cfg.all_sensors = [sensor_cfg]

        SensorFactory.init_sensors(cfg)

        reference_element: Element = sensor_element_pair.element
        element: Element = data_reader.get_element(sensor)

        if isinstance(element.measurement.values[0], Image):
            assert DataFactory.equal_images(element, reference_element) is True
        else:
            assert element.measurement.values == reference_element.measurement.values

        assert element.timestamp == reference_element.timestamp
        assert element.location == reference_element.location
        assert element.measurement.sensor == reference_element.measurement.sensor

    @mark.parametrize("sensor_element_pair", (sensor_element_pairs))
    def test_get_element_4(
        self,
        data_reader: KaistReader,
        sensor_element_pair: SensorElementPair,
    ):
        sensor: Sensor = sensor_element_pair.sensor

        sensor_cfg: SensorConfig = SensorConfig(
            name=sensor.name, type=sensor.__class__.__name__, config=ParameterConfig()
        )
        cfg: SensorFactoryConfig = SensorFactoryConfig()
        cfg.used_sensors = [sensor_cfg]
        cfg.all_sensors = [sensor_cfg]

        SensorFactory.init_sensors(cfg)

        reference_element: Element = sensor_element_pair.element
        timestamp: int = reference_element.timestamp
        element: Element = data_reader.get_element(sensor, timestamp)

        if isinstance(element.measurement.values[0], Image):
            assert DataFactory.equal_images(element, reference_element) is True
        else:
            assert element.measurement.values == reference_element.measurement.values

        assert element.timestamp == reference_element.timestamp
        assert element.location == reference_element.location
        assert element.measurement.sensor == reference_element.measurement.sensor
