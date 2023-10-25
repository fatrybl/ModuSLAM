import pytest
from pathlib import Path
from rosbags.serde import deserialize_cdr, ros1_to_cdr
from typing import Type

from slam.data_manager.factory.readers.ros1.ros1_reader import Ros1BagReader
from slam.data_manager.factory.readers.element_factory import Element, Measurement
from tests.data_manager.Ros1Reader.data_factory import TestDataFactory
from slam.utils.exceptions import FileNotValid, TopicNotFound, NotSubset
from slam.data_manager.factory.readers.ros1.dataset_iterator import RosElementLocation
from slam.setup_manager.sensor_factory.sensors import (
    Sensor, Imu, Fog, Encoder, StereoCamera, Altimeter, Gps, VrsGps, Lidar2D, Lidar3D)
from slam.utils.auxiliary_dataclasses import TimeRange
from slam.setup_manager.sensor_factory.sensor_factory import SensorFactory
from configs.system.data_manager.manager import Regime, Stream
from configs.experiments.ros1.config import Ros1DS

def test_unknown_file_scenario():
    cfg: Ros1DS  = TestDataFactory.get_default_config()
    cfg.directory = Path( "/non_exist_dir" )
    regime: Regime = Stream()
    with pytest.raises(FileNotValid):
        reader = Ros1BagReader(cfg, regime)



def test_unknown_topic_scenario():
    cfg: Ros1DS  = TestDataFactory.get_default_config()
    cfg.used_sensors[0].topic = "/unexist_topic"
    regime: Regime = Stream()
    with pytest.raises(TopicNotFound):
        reader = Ros1BagReader(cfg, regime)



def test_ros_get_elements_in_time():
    cfg: Ros1DS  = TestDataFactory.get_default_config()
    regime: Regime = Stream()

    reader = Ros1BagReader(cfg, regime)
    sensor_imu: Imu = SensorFactory.name_to_sensor(TestDataFactory.imu.name)
    sensor_lidar: Lidar2D = SensorFactory.name_to_sensor(TestDataFactory.lidar_2D_middle.name)
    sensor_gps: Gps = SensorFactory.name_to_sensor(TestDataFactory.gps.name)
    
    time_range = TimeRange(start = 2, stop = 6)
    element_list = []
    
    element: Element = reader.get_element(sensor_imu, time_range.start)
    element_list.append(element)

    while(element.timestamp < time_range.stop):
        element: Element = reader.get_element(sensor_imu, None)
        if(element is None):
            break
        else:
            element_list.append(element)

    assert len(element_list) == 2


    time_range = TimeRange(4, 20)
    element_list = []
    element: Element = reader.get_element(sensor_gps, time_range.start)
    current_timestamp = element.timestamp
    element_list.append(element)

    while 1:
        element: Element = reader.get_element(sensor_gps, None)
        current_timestamp = element.timestamp
        if(current_timestamp > time_range.stop):
            break
        element_list.append(element)

    assert len(element_list) == 4

    time_range = TimeRange(4, 20)
    element_list = []

    element: Element = reader.get_element(sensor_lidar, time_range.start)
    current_timestamp = element.timestamp
    element_list.append(element)

    while 1:
        element: Element = reader.get_element(sensor_lidar, None)
        current_timestamp = element.timestamp
        if(current_timestamp > time_range.stop):
            break
        element_list.append(element)

    assert len(element_list) == 3



scenario_all_sensors = ([TestDataFactory.imu, TestDataFactory.stereo, TestDataFactory.gps, TestDataFactory.lidar_2D_middle], 20)   
scenario_half_sensors = ([TestDataFactory.imu, TestDataFactory.stereo], 10)

success_scenarios = [scenario_all_sensors, scenario_half_sensors]
@pytest.mark.parametrize(
    ("test_sensors", "expected_elements_amount"), success_scenarios
)
def test_ros_elements_amount(test_sensors: list[str], expected_elements_amount):
    cfg: Ros1DS  =  TestDataFactory.get_default_config()
    regime: Regime = Stream()
    cfg.used_sensors = test_sensors
    reader = Ros1BagReader(cfg, regime)
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
    cfg: Ros1DS  =  TestDataFactory.get_default_config()
    regime: Regime = Stream()
    reader = Ros1BagReader(cfg, regime)

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
    ros_msg = deserialize_cdr(ros1_to_cdr(read_element.measurement.values, read_element.location.msgtype), read_element.location.msgtype)
    latitude, longitude, altitude = ros_msg.latitude, ros_msg.longitude, ros_msg.altitude
    assert [latitude, longitude, altitude] == TestDataFactory.GNSS_POSITION



def test_close_loop():
    cfg: Ros1DS  =  TestDataFactory.get_default_config()
    regime: Regime = Stream()
    reader = Ros1BagReader(cfg, regime)
    element_cnt = 0
    expected_elements_amount = 20
    while True:
        request_element = Element(timestamp=9, location = RosElementLocation(file = TestDataFactory.FILE1, topic = TestDataFactory.GNSS_TOPIC, msgtype="some_msg_type"), measurement = ())
        read_element = reader.get_element(request_element)
        ros_msg = deserialize_cdr(ros1_to_cdr(read_element.measurement.values, read_element.location.msgtype),  read_element.location.msgtype)
        latitude, longitude, altitude = ros_msg.latitude, ros_msg.longitude, ros_msg.altitude
        assert [latitude, longitude, altitude] == TestDataFactory.GNSS_POSITION

        request_element = Element(timestamp=15, location=RosElementLocation(file = TestDataFactory.FILE2, topic = TestDataFactory.IMU_TOPIC, msgtype="some_msg_type"), measurement = ())
        read_element = reader.get_element(request_element)

        ros_msg = deserialize_cdr(ros1_to_cdr(read_element.measurement.values, read_element.location.msgtype), read_element.location.msgtype)
        w_x, w_y, w_z = ros_msg.angular_velocity.x, ros_msg.angular_velocity.y, ros_msg.angular_velocity.z
        assert [w_x, w_y, w_z] == TestDataFactory.IMU_DATA

        element = reader.get_element()
        if(element == None):
            break
        element_cnt+=1

    assert element_cnt == expected_elements_amount

