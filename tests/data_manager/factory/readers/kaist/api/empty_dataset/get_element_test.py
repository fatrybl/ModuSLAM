from pytest import mark, raises
from pathlib import Path

from slam.data_manager.factory.readers.element_factory import Element, Measurement
from slam.data_manager.factory.readers.kaist.data_classes import CsvDataLocation

from slam.data_manager.factory.readers.kaist.kaist_reader import KaistReader
from slam.setup_manager.sensor_factory.sensor_factory import SensorFactory
from slam.setup_manager.sensor_factory.sensors import Imu
from slam.utils.exceptions import FileNotValid

from .config_factory import imu

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


class TestGetElement:

    def test_get_element_1(self, data_reader: KaistReader):
        """
        Tries to get an element from a dataaset. 
        Raises an exception as "data_stamp.csv" is not valid (empty).

        Args:
            data_reader (KaistReader): reader to an element from a dataaset.
        """
        with raises(FileNotValid):
            data_reader.get_element()

    @mark.xfail
    def test_get_element_2(self, data_reader: KaistReader, sensor_factory: SensorFactory):
        """
        Test must fail as the dataset is empty.
        get_element() method accepts only those elements which exist in the dataset.
        """
        sensor = sensor_factory.name_to_sensor(imu.name)
        m = Measurement(sensor, values=(1, 2, 3))
        loc = CsvDataLocation(file=Path(), position=0)
        t: int = 1

        element = Element(timestamp=t,
                          measurement=m,
                          location=loc)

        data_reader.get_element(element)

    @mark.xfail
    def test_get_element_3(self, data_reader: KaistReader, sensor_factory: SensorFactory):
        """
        Test must fail as the dataset is empty.
        get_element() method accepts only those elements which have existed in the dataset before.
        """
        sensor: Imu = sensor_factory.name_to_sensor(imu.name)
        data_reader.get_element(sensor)

    @mark.xfail
    def test_get_element_4(self, data_reader: KaistReader, sensor_factory: SensorFactory):
        """
        Test must fail as the dataset is empty.
        get_element() method accepts only those elements which have existed in the dataset before.
        """
        t: int = 1
        sensor: Imu = sensor_factory.name_to_sensor(imu.name)
        data_reader.get_element(sensor=sensor,
                                timestamp=t)
