from typing import Type
from pytest import mark
from unittest.mock import Mock, patch


from slam.data_manager.factory.readers.element_factory import Element
from slam.data_manager.factory.readers.kaist.kaist_reader import KaistReader
from slam.setup_manager.sensor_factory.sensors import Sensor


from slam.utils.kaist_data_factory import DataFactory, SensorElementPair

from .data import (elements, sensor_element_pairs)


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


OBJECT_PATH_TO_PATCH = "slam.data_manager.factory.readers.kaist.kaist_reader.SensorFactory"


class TestGetElement:
    """
    KaistReader object is used as a fixture with scope "class" to be created once. 
    This prevents the creation of KaistReader objects every time the test is called with new parameters
    ==> prevents resetig of iterators for get_element() method.
    """

    @mark.parametrize("reference_element",
                      (elements))
    @patch(OBJECT_PATH_TO_PATCH)
    def test_get_element_1(self, mock_sensor_factory: Mock, data_reader: KaistReader, reference_element: Element):
        sensor: Type[Sensor] = reference_element.measurement.sensor
        mock_sensor_factory.used_sensors = {sensor}
        mock_sensor_factory.name_to_sensor.return_value = sensor

        element: Element = data_reader.get_element()

        values = list(DataFactory.flatten(element.measurement.values))
        true_values = list(DataFactory.flatten(
            reference_element.measurement.values))

        assert element.timestamp == reference_element.timestamp
        assert element.location == reference_element.location
        assert element.measurement.sensor == reference_element.measurement.sensor
        assert values == true_values

    @mark.parametrize("reference_element",
                      (elements))
    @patch(OBJECT_PATH_TO_PATCH)
    def test_get_element_2(self, mock_sensor_factory: Mock, data_reader: KaistReader, reference_element: Element):
        sensor: Type[Sensor] = reference_element.measurement.sensor
        mock_sensor_factory.used_sensors = {sensor}
        mock_sensor_factory.name_to_sensor.return_value = sensor

        element: Element = data_reader.get_element(reference_element)

        values = list(DataFactory.flatten(element.measurement.values))
        true_values = list(DataFactory.flatten(
            reference_element.measurement.values))

        assert element.timestamp == reference_element.timestamp
        assert element.location == reference_element.location
        assert element.measurement.sensor == reference_element.measurement.sensor
        assert values == true_values


class TestGetElementOfSensor:
    """
    KaistReader object is used as a fixture with scope "class" to be created once. 
    This prevents the creation of KaistReader objects every time the test is called with new parameters
    ==> prevents resetig of iterators for get_element() method.
    """

    @mark.parametrize("sensor_element_pair",
                      (sensor_element_pairs))
    @patch(OBJECT_PATH_TO_PATCH)
    def test_get_element_3(self, mock_sensor_factory: Mock, data_reader: KaistReader, sensor_element_pair: SensorElementPair):
        sensor: Type[Sensor] = sensor_element_pair.sensor
        mock_sensor_factory.used_sensors = {sensor}
        mock_sensor_factory.name_to_sensor.return_value = sensor

        reference_element: Element = sensor_element_pair.element
        element: Element = data_reader.get_element(sensor)

        values = list(DataFactory.flatten(element.measurement.values))
        true_values = list(DataFactory.flatten(
            reference_element.measurement.values))

        assert element.timestamp == reference_element.timestamp
        assert element.location == reference_element.location
        assert element.measurement.sensor == reference_element.measurement.sensor
        assert values == true_values

    @mark.parametrize("sensor_element_pair",
                      (sensor_element_pairs))
    @patch(OBJECT_PATH_TO_PATCH)
    def test_get_element_4(self, mock_sensor_factory: Mock, data_reader: KaistReader, sensor_element_pair: SensorElementPair):
        sensor: Type[Sensor] = sensor_element_pair.sensor
        mock_sensor_factory.used_sensors = {sensor}
        mock_sensor_factory.name_to_sensor.return_value = sensor

        reference_element: Element = sensor_element_pair.element
        timestamp: int = reference_element.timestamp
        element: Element = data_reader.get_element(sensor, timestamp)

        values = list(DataFactory.flatten(element.measurement.values))
        true_values = list(DataFactory.flatten(
            reference_element.measurement.values))

        assert element.timestamp == reference_element.timestamp
        assert element.location == reference_element.location
        assert element.measurement.sensor == reference_element.measurement.sensor
        assert values == true_values
