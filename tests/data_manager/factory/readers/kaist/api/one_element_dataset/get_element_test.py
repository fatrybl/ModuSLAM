from typing import Any, Iterable, Type
from collections.abc import Iterator
from pytest import mark

from slam.data_manager.factory.readers.kaist.kaist_reader import KaistReader
from slam.data_manager.factory.readers.element_factory import Element, Measurement
from slam.setup_manager.sensor_factory.sensor_factory import SensorFactory
from slam.setup_manager.sensor_factory.sensors import Sensor

from tests.data_manager.factory.readers.kaist.api.one_element_dataset.data_factory import (
    PseudoElement, DataFactory, SensorElementPair)
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


def convert_to_element(element: PseudoElement, sensor_factory: SensorFactory) -> Element:
    """
    Convert a PseudoElement to an Element based on SensorFactory and pseudo_element.sensor_name attribute.

    Args:
        element (PseudoElement): element without Sensor but sensor_name attribute.
        sensor_factory (SensorFactory): Sensor factory maps sensor name to Sensor.

    Returns:
        Element: correct element with proper Sensor.
    """
    sensor: Type[Sensor] = sensor_factory.name_to_sensor(
        element.measurement.sensor_name)
    real_element = Element(element.timestamp,
                           Measurement(sensor, element.measurement.values),
                           element.location)
    return real_element


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

    @mark.parametrize(
        ("reference_element"),
        DataFactory.elements)
    def test_get_element_1(self, data_reader: KaistReader, sensor_factory: SensorFactory, reference_element: PseudoElement):
        input_element: Element = convert_to_element(
            reference_element, sensor_factory)
        element: Element = data_reader.get_element()
        expected_values = list(flatten(element.measurement.values))
        true_values = list(flatten(input_element.measurement.values))
        print('================================================================\n')
        print(element.location)
        print(input_element.location)
        assert element.timestamp == input_element.timestamp
        assert element.location == input_element.location
        assert element.measurement.sensor == input_element.measurement.sensor
        assert expected_values == true_values

    @mark.parametrize(
        ("reference_element"),
        DataFactory.elements)
    def test_get_element_2(self, data_reader: KaistReader, sensor_factory: SensorFactory, reference_element: PseudoElement):
        input_element: Element = convert_to_element(
            reference_element, sensor_factory)
        element: Element = data_reader.get_element(input_element)
        expected_values = list(flatten(element.measurement.values))
        true_values = list(flatten(input_element.measurement.values))
        assert element.timestamp == input_element.timestamp
        assert element.location == input_element.location
        assert element.measurement.sensor == input_element.measurement.sensor
        assert expected_values == true_values


class TestGetElementOfSensor:

    @mark.parametrize(
        ("sensor_element_pair"),
        DataFactory.sensor_element_pairs)
    def test_get_element_3(self, data_reader: KaistReader, sensor_factory: SensorFactory, sensor_element_pair: SensorElementPair):
        sensor_name: str = sensor_element_pair.sensor.name
        reference_element: PseudoElement = sensor_element_pair.element
        sensor: Type[Sensor] = sensor_factory.name_to_sensor(sensor_name)
        input_element: Element = convert_to_element(
            reference_element, sensor_factory)
        element: Element = data_reader.get_element(sensor)
        expected_values = list(flatten(element.measurement.values))
        true_values = list(flatten(input_element.measurement.values))
        assert element.timestamp == input_element.timestamp
        assert element.location == input_element.location
        assert element.measurement.sensor == input_element.measurement.sensor
        assert expected_values == true_values

    @mark.parametrize(
        ("sensor_element_pair"),
        DataFactory.sensor_element_pairs)
    def test_get_element_4(self, data_reader: KaistReader, sensor_factory: SensorFactory, sensor_element_pair: SensorElementPair):
        sensor_name: str = sensor_element_pair.sensor.name
        reference_element: PseudoElement = sensor_element_pair.element
        timestamp: int = sensor_element_pair.element.timestamp
        sensor: Type[Sensor] = sensor_factory.name_to_sensor(sensor_name)
        input_element: Element = convert_to_element(
            reference_element, sensor_factory)
        element: Element = data_reader.get_element(sensor,
                                                   timestamp)
        expected_values = list(flatten(element.measurement.values))
        true_values = list(flatten(input_element.measurement.values))
        assert element.timestamp == input_element.timestamp
        assert element.location == input_element.location
        assert element.measurement.sensor == input_element.measurement.sensor
        assert expected_values == true_values
