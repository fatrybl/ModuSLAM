import pytest

from numpy import array as numpy_array
from numpy import array_equal, dstack

from tests.data_manager.KaistReader.data_factory import TestDataFactory

scenario1 = ([1234, '0.1234', '-0.1234', '0.1234'], 'imu')
scenario2 = ([1234, '0.1234', '-0.1234', '0.1234'], 'fog')
scenario3 = ([1234, '0.1234', '-0.1234', '0.1234'], 'gps')
scenario4 = ([1234, '0.1234', '-0.1234', '0.1234'], 'vrs')
scenario5 = ([1234, '0.1234', '-0.1234', '0.1234'], 'altimeter')
scenario6 = ([1234, '0.1234', '-0.1234', '0.1234'], 'encoder')

scenario7 = (1234, TestDataFactory.to_bytes_array(
    [1234, 0.1234, -0.1234, 0.1234]), 'sick_back')
scenario8 = (1234, TestDataFactory.to_bytes_array(
    [1234, 0.1234, -0.1234, 0.1234]), 'sick_middle')
scenario9 = (1234, TestDataFactory.to_bytes_array(
    [1234, 0.1234, -0.1234, 0.1234]), 'velodyne_left')
scenario10 = (1234, TestDataFactory.to_bytes_array(
    [1234, 0.1234, -0.1234, 0.1234]), 'velodyne_right')

success_scenarios_csv = [scenario1, scenario2,
                         scenario3, scenario4,
                         scenario5, scenario6]

success_scenarios_bin = [scenario7, scenario8,
                         scenario9, scenario10]


gray_img = numpy_array([0, 255, 255, 0]).reshape(2, 2)
rgb_img = dstack([gray_img, gray_img, gray_img])
scenario11 = (1234, rgb_img, 'stereo')

success_scenarios_png = [scenario11]


@pytest.mark.parametrize(("test_data", "sensor"), success_scenarios_csv)
def test_get_element_csv(prepare_data, kaist_reader, clean, test_data, sensor):
    element = kaist_reader.get_element()
    expected_timestamp = test_data[0]
    assert expected_timestamp == element.timestamp
    assert test_data[1:] == element.measurement.values
    assert sensor == element.measurement.sensor


@pytest.mark.parametrize(("expected_timestamp", "test_data", "sensor"), success_scenarios_bin)
def test_get_element_bin(prepare_data, kaist_reader, clean, expected_timestamp, test_data, sensor):
    element = kaist_reader.get_element()
    assert expected_timestamp == element.timestamp
    assert sensor == element.measurement.sensor
    assert test_data == element.measurement.values


@pytest.mark.parametrize(("expected_timestamp", "test_data", "sensor"), success_scenarios_png)
def test_get_element_png(prepare_data, kaist_reader, clean, expected_timestamp, test_data, sensor):
    element = kaist_reader.get_element()
    first_img = element.measurement.values[0]
    second_img = element.measurement.values[1]
    assert array_equal(first_img, test_data)
    assert array_equal(second_img, test_data)
    assert expected_timestamp == element.timestamp
    assert sensor == element.measurement.sensor
