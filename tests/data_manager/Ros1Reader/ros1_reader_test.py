import pytest
from pathlib import Path
import dataclasses
from rosbags.serde import deserialize_cdr, ros1_to_cdr

from slam.data_manager.factory.readers.ros1.ros1_reader import Ros1BagReader
from slam.data_manager.factory.readers.element_factory import Element, Measurement
from tests.data_manager.Ros1Reader.data_factory import TestDataFactory
from slam.utils.exceptions import FileNotValid, TopicNotFound, NotSubset
from slam.data_manager.factory.readers.ros1.dataset_iterator import RosElementLocation
from slam.setup_manager.sensor_factory.sensors import (
    Sensor, Imu, Fog, Encoder, StereoCamera, Altimeter, Gps, VrsGps, Lidar2D, Lidar3D)
from slam.utils.auxiliary_dataclasses import TimeRange
from configs.experiments.ros1.config import Ros1

def test_unknown_file_scenario():
    cfg: Ros1  = TestDataFactory.get_default_config()
    cfg.data_manager.dataset.directory = Path( "/non_exist_dir" )
    with pytest.raises(FileNotValid):
        reader = Ros1BagReader(cfg)



def test_unknown_topic_scenario():
    cfg =dataclasses.replace( TestDataFactory.get_default_config())
    cfg.setup_manager.all_sensors[0].topic = "/unexist_topic"
    with pytest.raises(TopicNotFound):
        reader = Ros1BagReader(cfg)



def test_ros_get_elements_in_time():
    reader = Ros1BagReader(TestDataFactory.get_default_config())

    time_range = TimeRange(2, 6)
    element_list = []
    element: Element = reader.get_element(time_range, Imu.__name__, True)
    element_list.append(element)

    while(element.timestamp < time_range.stop):
        element: Element = reader.get_element(time_range, Imu.__name__)
        if(element is None):
            break
        else:
            element_list.append(element)

    assert len(element_list) == 2


    time_range = TimeRange(4, 20)
    element_list = []
    element: Element = reader.get_element(time_range, Gps.__name__, True)
    element_list.append(element)

    while(element.timestamp < time_range.stop):
        element: Element = reader.get_element(time_range, Imu.__name__)
        if(element is None):
            break
        else:
            element_list.append(element)

    assert len(element_list) == 4

    time_range = TimeRange(4, 20)
    element_list = []
    element: Element = reader.get_element(time_range, Lidar2D.__name__, True)
    element_list.append(element)

    while(element.timestamp < time_range.stop):
        element: Element = reader.get_element(time_range, Imu.__name__)
        if(element is None):
            break
        else:
            element_list.append(element)

    assert len(element_list) == 3



scenario_all_sensors = ([TestDataFactory.imu, TestDataFactory.stereo, TestDataFactory.gps, TestDataFactory.lidar_2D_middle], 20)   
scenario_half_sensors = ([TestDataFactory.imu, TestDataFactory.stereo], 10)

success_scenarios = [scenario_all_sensors, scenario_half_sensors]
@pytest.mark.parametrize(
    ("test_sensors", "expected_elements_amount"), success_scenarios
)
def test_ros_elements_amount(test_sensors: list[str], expected_elements_amount):
    cfg: Ros1  =  TestDataFactory.get_default_config()
    cfg.setup_manager.used_sensors = test_sensors
    reader = Ros1BagReader(cfg)
    element_cnt = 0
    while True:
        element = reader.get_element()
        if(element == None):
            break
        else:
            pass
        element_cnt+=1
    assert element_cnt == expected_elements_amount



def test_ros_get_element_with_arg():
    reader = Ros1BagReader(TestDataFactory.get_default_config())

    with pytest.raises(KeyError):
        loc = RosElementLocation(file = TestDataFactory.FILE1, topic = "/unexist_topic", msgtype="some_msg_type")
        request_element_wrong_topic = Element(timestamp=300, measurement = (), location=loc)
        read_element = reader.get_element(request_element_wrong_topic)

    request_element_wrong_timestamp = Element(timestamp=30000, location=RosElementLocation(file = TestDataFactory.FILE1, topic = TestDataFactory.CAMERA_TOPIC, msgtype="some_msg_type"), measurement = ())
    read_element = reader.get_element(request_element_wrong_timestamp)
    assert read_element == None

    request_element = Element(timestamp=2, location=RosElementLocation(file = TestDataFactory.FILE1, topic = TestDataFactory.IMU_TOPIC, msgtype="some_msg_type"), measurement = ())
    read_element = reader.get_element(request_element)
    assert read_element.measurement.values == b'123456789ABCDEQGEGKJBNKJBN'

    request_element = Element(timestamp=4, location=RosElementLocation(file = TestDataFactory.FILE1, topic = TestDataFactory.CAMERA_TOPIC, msgtype="some_msg_type"), measurement = ())
    read_element = reader.get_element(request_element)
    assert read_element.measurement.values == b'JFVNKJGJHK'

    request_element = Element(timestamp=14, location=RosElementLocation(file = TestDataFactory.FILE2, topic = TestDataFactory.GNSS_TOPIC, msgtype="some_msg_type"), measurement = ())
    read_element = reader.get_element(request_element)
    assert read_element.measurement.values == b'iubgkhnlkml'

    request_element = Element(timestamp=23, location=RosElementLocation(file = TestDataFactory.FILE3, topic = TestDataFactory.CAMERA_TOPIC, msgtype="some_msg_type"), measurement = ())
    read_element = reader.get_element(request_element)
    assert read_element.measurement.values == b'KJHKJ'

    request_element = Element(timestamp=9, location=RosElementLocation(file = TestDataFactory.FILE1, topic = TestDataFactory.GNSS_TOPIC, msgtype="some_msg_type"), measurement = ())
    read_element = reader.get_element(request_element)
    read_element.measurement.values = deserialize_cdr(ros1_to_cdr(read_element.measurement.values, read_element.location.msgtype), read_element.location.msgtype)
    latitude, longitude, altitude = read_element.measurement.values.latitude, read_element.measurement.values.longitude, read_element.measurement.values.altitude
    assert [latitude, longitude, altitude] == TestDataFactory.GNSS_POSITION



def test_close_loop():
    reader = Ros1BagReader(TestDataFactory.get_default_config())
    element_cnt = 0
    expected_elements_amount = 20
    while True:
        request_element = Element(timestamp=9, location = RosElementLocation(file = TestDataFactory.FILE1, topic = TestDataFactory.GNSS_TOPIC, msgtype="some_msg_type"), measurement = ())
        read_element = reader.get_element(request_element)
        read_element.measurement.values = deserialize_cdr(ros1_to_cdr(read_element.measurement.values, read_element.location.msgtype), read_element.location.msgtype)
        latitude, longitude, altitude = read_element.measurement.values.latitude, read_element.measurement.values.longitude, read_element.measurement.values.altitude
        assert [latitude, longitude, altitude] == TestDataFactory.GNSS_POSITION

        request_element = Element(timestamp=15, location=RosElementLocation(file = TestDataFactory.FILE2, topic = TestDataFactory.IMU_TOPIC, msgtype="some_msg_type"), measurement = ())
        read_element = reader.get_element(request_element)
        read_element.measurement.values = deserialize_cdr(ros1_to_cdr(read_element.measurement.values, read_element.location.msgtype), read_element.location.msgtype)
        w_x, w_y, w_z = read_element.measurement.values.angular_velocity.x, read_element.measurement.values.angular_velocity.y, read_element.measurement.values.angular_velocity.z
        assert [w_x, w_y, w_z] == TestDataFactory.IMU_DATA

        element = reader.get_element()
        if(element == None):
            break
        element_cnt+=1

    assert element_cnt == expected_elements_amount

