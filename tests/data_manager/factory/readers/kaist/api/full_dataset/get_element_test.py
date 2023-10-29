from typing import Any, Iterable, Type
from collections.abc import Iterator
from pytest import mark
from unittest.mock import Mock, patch

from slam.data_manager.factory.readers.element_factory import Element
from slam.data_manager.factory.readers.kaist.kaist_reader import KaistReader
from slam.setup_manager.sensor_factory.sensors import Sensor

from .data_factory import SensorElementPair

from tests.data_manager.factory.readers.kaist.api.full_dataset.data_factory import DataFactory
"""
How to test any DataReader:
1) Create a dataset for a DataReader.
2) Initialize config files for DataReader and SensorFactory.
3.1) Initialize SensorFactory object.
3.2) Initialize DataReader object with config file.
4) Test methods:
    4.1) get_element()
    4.2) get_element(element[Element])
    4.3) get_element(sensor[Sensor])
    4.4) get_element(sensor[Sensor], timestamp[int])
"""


def flatten(set: tuple[Any, ...]) -> Iterator[Any]:
    """
    Flattens tuple of tuples for propper comparison,
    Args:
        set (tuple[Any]): tuple of any-type-measurements

    Yields:
        Iterator[Any]: _description_
    """
    for item in set:
        if isinstance(item, Iterable) and not isinstance(item, str):
            for x in flatten(item):
                yield x
        else:
            yield item


class TestGetElement:

    @mark.parametrize("reference_element",
                      (DataFactory.elements))
    @patch("slam.data_manager.factory.readers.kaist.kaist_reader.SensorFactory")
    def test_get_element_1(self, mock_sensor_factory: Mock, data_reader: KaistReader, reference_element: Element):
        sensor: Type[Sensor] = reference_element.measurement.sensor

        mock_sensor_factory.used_sensors = {sensor}
        mock_sensor_factory.name_to_sensor.return_value = sensor

        element: Element = data_reader.get_element()

        values = list(flatten(element.measurement.values))
        true_values = list(flatten(reference_element.measurement.values))

        assert element.timestamp == reference_element.timestamp
        assert element.location == reference_element.location
        assert element.measurement.sensor == reference_element.measurement.sensor
        assert values == true_values

    @mark.parametrize("reference_element",
                      (DataFactory.elements))
    @patch("slam.data_manager.factory.readers.kaist.kaist_reader.SensorFactory")
    def test_get_element_2(self, mock_sensor_factory, data_reader: KaistReader, reference_element: Element):
        sensor: Type[Sensor] = reference_element.measurement.sensor

        mock_sensor_factory.used_sensors = {sensor}
        mock_sensor_factory.name_to_sensor.return_value = sensor

        element: Element = data_reader.get_element(reference_element)

        values = list(flatten(element.measurement.values))
        true_values = list(flatten(reference_element.measurement.values))

        assert element.timestamp == reference_element.timestamp
        assert element.location == reference_element.location
        assert element.measurement.sensor == reference_element.measurement.sensor
        assert values == true_values


class TestGetElementOfSensor:
    @mark.parametrize("sensor_element_pair",
                      (DataFactory.sensor_element_pairs))
    @patch("slam.data_manager.factory.readers.kaist.kaist_reader.SensorFactory")
    def test_get_element_3(self, mock_sensor_factory, data_reader: KaistReader, sensor_element_pair: SensorElementPair):
        sensor: Type[Sensor] = sensor_element_pair.sensor
        reference_element: Element = sensor_element_pair.element

        mock_sensor_factory.used_sensors = {sensor}
        mock_sensor_factory.name_to_sensor.return_value = sensor

        element: Element = data_reader.get_element(sensor)

        values = list(flatten(element.measurement.values))
        true_values = list(flatten(reference_element.measurement.values))

        assert element.timestamp == reference_element.timestamp
        assert element.location == reference_element.location
        assert element.measurement.sensor == reference_element.measurement.sensor
        assert values == true_values

    @mark.parametrize("sensor_element_pair",
                      (DataFactory.sensor_element_pairs))
    @patch("slam.data_manager.factory.readers.kaist.kaist_reader.SensorFactory")
    def test_get_element_4(self, mock_sensor_factory, data_reader: KaistReader, sensor_element_pair: SensorElementPair):
        sensor: Type[Sensor] = sensor_element_pair.sensor
        reference_element: Element = sensor_element_pair.element
        timestamp: int = reference_element.timestamp

        mock_sensor_factory.used_sensors = {sensor}
        mock_sensor_factory.name_to_sensor.return_value = sensor

        element: Element = data_reader.get_element(sensor, timestamp)

        values = list(flatten(element.measurement.values))
        true_values = list(flatten(reference_element.measurement.values))

        assert element.timestamp == reference_element.timestamp
        assert element.location == reference_element.location
        assert element.measurement.sensor == reference_element.measurement.sensor
        assert values == true_values
