import pytest
from pathlib import Path

from rosbags.serde import deserialize_cdr, ros1_to_cdr

from slam.data_manager.factory.readers.ros1.ros1_reader import Ros1BagReader, RosConfig
from slam.data_manager.factory.readers.element_factory import Element, Measurement
from tests.data_manager.Ros1Reader.data_factory import TestDataFactory, get_default_config
from slam.utils.exceptions import FileNotValid, TopicNotFound, NotSubset
from slam.data_manager.factory.readers.ros1.dataset_iterator import RosElementLocation
from slam.setup_manager.sensor_factory.sensors import (
    Sensor, Imu, Fog, Encoder, StereoCamera, Altimeter, Gps, VrsGps, Lidar2D, Lidar3D)

def test_unknown_file_scenario():
    cfg: RosConfig  = get_default_config()
    cfg.master_file_dir = Path( "/non_exist_dir" )
    with pytest.raises(FileNotValid):
        reader = Ros1BagReader(cfg)



def test_unknown_topic_scenario():
    cfg: RosConfig  = get_default_config()
    cfg.topic_sensor_cfg["camera"] = "unknown_topic"
    with pytest.raises(TopicNotFound):
        reader = Ros1BagReader(cfg)


def test_unknown_sensor_scenario():
    cfg: RosConfig  = get_default_config()
    cfg.sensors.append("unknown_sensor")
    with pytest.raises(NotSubset):
        reader = Ros1BagReader(cfg)



def test_ros_get_elements_in_time():
    reader = Ros1BagReader(get_default_config())
    element_list: list[Element] = reader.get_elements(2, 6)
    assert len(element_list) == 5

    element_list: list[Element] = reader.get_elements(0, 8)
    assert len(element_list) == 7

    element_list: list[Element] = reader.get_elements(7, 12)
    assert len(element_list) == 5

    element_list: list[Element] = reader.get_elements(14, 100)
    assert len(element_list) == 9

    element_list: list[Element] = reader.get_elements(14, 14)
    assert len(element_list) == 1

    element_list: list[Element] = reader.get_elements(14, 100)
    assert len(element_list) == 9
    # print()
    # for element in element_list:
    #     print(element)

scenario_all_topics = (["imu", "camera", "lidar", "gps"], 20)
scenario_half_topics = (["imu", "camera"], 10)
success_scenarios = [scenario_all_topics, scenario_half_topics]
@pytest.mark.parametrize(
    ("test_sensors", "expected_elements_amount"), success_scenarios
)
def test_ros_elements_amount(test_sensors: list[str], expected_elements_amount):
    cfg: RosConfig  = get_default_config()
    cfg.sensors = test_sensors
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
    reader = Ros1BagReader(get_default_config())

    with pytest.raises(KeyError):
        loc = RosElementLocation(file = TestDataFactory.FILE1, topic = "/unexist_topic", msgtype="some_msg_type", timestamp = 300)
        request_element_wrong_topic = Element(timestamp=300, measurement = (), location=loc)
        read_element = reader.get_element(request_element_wrong_topic)

    request_element_wrong_timestamp = Element(timestamp=30000, location=RosElementLocation(file = TestDataFactory.FILE1, topic = TestDataFactory.CAMERA_TOPIC, msgtype="some_msg_type", timestamp = 300), measurement = ())
    read_element = reader.get_element(request_element_wrong_timestamp)
    assert read_element == None

    request_element = Element(timestamp=2, location=RosElementLocation(file = TestDataFactory.FILE1, topic = TestDataFactory.IMU_TOPIC, msgtype="some_msg_type", timestamp = 2), measurement = ())
    read_element = reader.get_element(request_element)
    assert read_element.measurement.values == b'123456789ABCDEQGEGKJBNKJBN'

    request_element = Element(timestamp=4, location=RosElementLocation(file = TestDataFactory.FILE1, topic = TestDataFactory.CAMERA_TOPIC, msgtype="some_msg_type", timestamp = 4), measurement = ())
    read_element = reader.get_element(request_element)
    assert read_element.measurement.values == b'JFVNKJGJHK'

    request_element = Element(timestamp=14, location=RosElementLocation(file = TestDataFactory.FILE2, topic = TestDataFactory.GNSS_TOPIC, msgtype="some_msg_type", timestamp = 14), measurement = ())
    read_element = reader.get_element(request_element)
    assert read_element.measurement.values == b'iubgkhnlkml'

    request_element = Element(timestamp=23, location=RosElementLocation(file = TestDataFactory.FILE3, topic = TestDataFactory.CAMERA_TOPIC, msgtype="some_msg_type", timestamp = 23), measurement = ())
    read_element = reader.get_element(request_element)
    assert read_element.measurement.values == b'KJHKJ'

    request_element = Element(timestamp=9, location=RosElementLocation(file = TestDataFactory.FILE1, topic = TestDataFactory.GNSS_TOPIC, msgtype="some_msg_type", timestamp = 9), measurement = ())
    read_element = reader.get_element(request_element)
    read_element.measurement.values = deserialize_cdr(ros1_to_cdr(read_element.measurement.values, read_element.location.msgtype), read_element.location.msgtype)
    latitude, longitude, altitude = read_element.measurement.values.latitude, read_element.measurement.values.longitude, read_element.measurement.values.altitude
    assert [latitude, longitude, altitude] == TestDataFactory.GNSS_POSITION



def test_close_loop():
    reader = Ros1BagReader(get_default_config())
    element_cnt = 0
    expected_elements_amount = 20
    while True:
        request_element = Element(timestamp=9, location = RosElementLocation(file = TestDataFactory.FILE1, topic = TestDataFactory.GNSS_TOPIC, msgtype="some_msg_type", timestamp = 9), measurement = ())
        read_element = reader.get_element(request_element)
        read_element.measurement.values = deserialize_cdr(ros1_to_cdr(read_element.measurement.values, read_element.location.msgtype), read_element.location.msgtype)
        latitude, longitude, altitude = read_element.measurement.values.latitude, read_element.measurement.values.longitude, read_element.measurement.values.altitude
        assert [latitude, longitude, altitude] == TestDataFactory.GNSS_POSITION

        request_element = Element(timestamp=15, location=RosElementLocation(file = TestDataFactory.FILE2, topic = TestDataFactory.IMU_TOPIC, msgtype="some_msg_type", timestamp = 15), measurement = ())
        read_element = reader.get_element(request_element)
        read_element.measurement.values = deserialize_cdr(ros1_to_cdr(read_element.measurement.values, read_element.location.msgtype), read_element.location.msgtype)
        w_x, w_y, w_z = read_element.measurement.values.angular_velocity.x, read_element.measurement.values.angular_velocity.y, read_element.measurement.values.angular_velocity.z
        assert [w_x, w_y, w_z] == TestDataFactory.IMU_DATA

        element = reader.get_element()
        if(element == None):
            break
        element_cnt+=1

    assert element_cnt == expected_elements_amount

