import pytest

from numpy import array as numpy_array
from numpy import array_equal, dstack, ndarray
from slam.data_manager.factory.readers.element_factory import Element, Measurement
from slam.data_manager.factory.readers.kaist.measurement_collector import CsvDataLocation
from slam.setup_manager.sensor_factory.sensors import Sensor

from tests.data_manager.factory.readers.kaist.data_factory import TestDataFactory

scenario1 = (TestDataFactory.imu, TestDataFactory.data_stamp[0][1])
scenario2 = (TestDataFactory.fog, TestDataFactory.data_stamp[1][1])
scenario3 = (TestDataFactory.gps, TestDataFactory.data_stamp[2][1])
scenario4 = (TestDataFactory.vrs_gps, TestDataFactory.data_stamp[3][1])
scenario5 = (TestDataFactory.altimeter, TestDataFactory.data_stamp[4][1])
scenario6 = (TestDataFactory.encoder, TestDataFactory.data_stamp[5][1])

scenario7 = (
    TestDataFactory.sick_back[0],
    TestDataFactory.to_bytes_array(TestDataFactory.sick_back),
    TestDataFactory.data_stamp[6][1]
)
scenario8 = (
    TestDataFactory.sick_middle[0],
    TestDataFactory.to_bytes_array(TestDataFactory.sick_middle),
    TestDataFactory.data_stamp[7][1]
)
scenario9 = (
    TestDataFactory.velodyne_left[0],
    TestDataFactory.to_bytes_array(TestDataFactory.velodyne_left),
    TestDataFactory.data_stamp[8][1]
)
scenario10 = (
    TestDataFactory.velodyne_right[0],
    TestDataFactory.to_bytes_array(TestDataFactory.velodyne_right),
    TestDataFactory.data_stamp[9][1]
)

success_scenarios_csv = [scenario1, scenario2,
                         scenario3, scenario4,
                         scenario5, scenario6]

success_scenarios_bin = [scenario7, scenario8,
                         scenario9, scenario10]


gray_img = numpy_array(TestDataFactory.stereo_left).reshape(2, 2)
rgb_img = dstack([gray_img, gray_img, gray_img])
scenario11 = (
    TestDataFactory.data_stamp[10][0],
    rgb_img,
    TestDataFactory.data_stamp[10][1]
)

success_scenarios_png = [scenario11]


@pytest.mark.parametrize(("test_data", "sensor"), success_scenarios_csv)
def test_get_element_csv(kaist_reader, test_data, sensor):
    element: Element = kaist_reader.get_element()
    expected_timestamp: int = test_data[0]
    test_data_without_time: list[int | float] = test_data[1:]
    float_values = [float(i) for i in element.measurement.values]
    assert expected_timestamp == element.timestamp
    assert test_data_without_time == float_values
    assert sensor == element.measurement.sensor.name


@pytest.mark.parametrize(("expected_timestamp", "test_data", "sensor"), success_scenarios_bin)
def test_get_element_bin(kaist_reader, expected_timestamp, test_data, sensor):
    element: Element = kaist_reader.get_element()
    assert expected_timestamp == element.timestamp
    assert sensor == element.measurement.sensor.name
    assert test_data == element.measurement.values


@pytest.mark.parametrize(("expected_timestamp", "test_data", "sensor"), success_scenarios_png)
def test_get_element_png(kaist_reader, expected_timestamp, test_data, sensor):
    element: Element = kaist_reader.get_element()
    first_img: ndarray = element.measurement.values[0]
    second_img: ndarray = element.measurement.values[1]
    expected_timestamp = int(expected_timestamp)
    assert array_equal(first_img, test_data)
    assert array_equal(second_img, test_data)
    assert expected_timestamp == element.timestamp
    assert sensor == element.measurement.sensor.name


class Imu(Sensor):
    def __init__(self, name: str):
        self.name = name


class Fog(Sensor):
    def __init__(self, name: str):
        self.name = name


scenario1 = (Element(
    TestDataFactory.imu[0],
    Measurement(Imu(TestDataFactory.data_stamp[0][1]), None),
    CsvDataLocation(TestDataFactory.csv_data[0][1], 0)),
    TestDataFactory.imu[1:])

scenario2 = (Element(
    TestDataFactory.fog[0],
    Measurement(Fog(TestDataFactory.data_stamp[1][1]), None),
    CsvDataLocation(TestDataFactory.csv_data[1][1], 0)),
    TestDataFactory.fog[1:])


success_scenarios_csv = [scenario1, scenario2]


@pytest.mark.parametrize(("element_without_data", "expected_data"), success_scenarios_csv)
def test_get_element(kaist_reader, element_without_data, expected_data):
    element_with_data: Element = kaist_reader.get_element(element_without_data)
    float_list = [float(i) for i in element_with_data.measurement.values]
    assert expected_data == float_list
