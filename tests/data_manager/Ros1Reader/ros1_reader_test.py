import pytest
from pathlib import Path

from rosbags.serde import deserialize_cdr, ros1_to_cdr
import hydra

from slam.data_manager.factory.readers.ros1.ros1_reader import Ros1BagReader
from slam.data_manager.factory.readers.element_factory import Element, Measurement
from tests.data_manager.Ros1Reader.data_factory import TestDataFactory, create_config_file
from slam.utils.exceptions import FileNotValid, TopicNotFound, NotSubset
from slam.data_manager.factory.readers.ros1.dataset_iterator import RosElementLocation

DEFAULT_TOPIC_CONFIG = {"ros1_reader": {
                                        "used_topics": {"imu": TestDataFactory.IMU_TOPIC,
                                                        "camera": TestDataFactory.CAMERA_TOPIC,
                                                        "lidar":  TestDataFactory.LIDAR_TOPIC,
                                                        "gnss": TestDataFactory.GNSS_TOPIC},
                                       },
                        "used_sensors": ["imu", "camera", "lidar", "gnss"]
                       }

def test_unknown_file_scenario():
    create_config_file(DEFAULT_TOPIC_CONFIG)
    path = Path(__file__).parent/ "non_exist.bag" 
    with pytest.raises(FileNotValid):
        reader = Ros1BagReader(data_reader_conf_path = TestDataFactory.DEFAULT_CONFIG_PATH, 
                               master_file_dir = path)



def test_unknown_topic_scenario():
    create_config_file({"ros1_reader": {
                                        "used_topics": {"imu": TestDataFactory.IMU_TOPIC,
                                                        "camera": "unknown_topic"},       
                                        },
                        "used_sensors": ["imu", "camera"]   
                          })
    with pytest.raises(TopicNotFound):
        reader = Ros1BagReader(data_reader_conf_path = TestDataFactory.DEFAULT_CONFIG_PATH,
                                deserialize_raw_data = False,
                                master_file_dir = TestDataFactory.MASTER_BAG_DIR)


def test_unknown_sensor_scenario():
    create_config_file({"ros1_reader": {
                                        "used_topics": {"imu": TestDataFactory.IMU_TOPIC,
                                                        "camera": TestDataFactory.CAMERA_TOPIC,},       
                                        },
                        "used_sensors": ["imu", "unknown_sonsor"]   
                          })
    with pytest.raises(NotSubset):
        reader = Ros1BagReader(data_reader_conf_path = TestDataFactory.DEFAULT_CONFIG_PATH,
                                deserialize_raw_data = False,
                                master_file_dir = TestDataFactory.MASTER_BAG_DIR)



scenario_all_topics = (DEFAULT_TOPIC_CONFIG, 20)
scenario_half_topics = ({"ros1_reader": {"used_topics": {"imu": TestDataFactory.IMU_TOPIC,
                                                          "camera":  TestDataFactory.CAMERA_TOPIC,
                                                          "lidar": TestDataFactory.LIDAR_TOPIC}
                                        },
                        "used_sensors": ["imu", "camera"]
                      }, 10)
success_scenarios = [scenario_all_topics, scenario_half_topics]

@pytest.mark.parametrize(
    ("test_cfg", "expected_elements_amount"), success_scenarios
)
def test_ros_elements_amount(test_cfg: dict[str, dict[str, str]], expected_elements_amount):
    create_config_file(test_cfg)
    reader = Ros1BagReader(data_reader_conf_path = TestDataFactory.DEFAULT_CONFIG_PATH,
                           deserialize_raw_data = False,
                           master_file_dir = TestDataFactory.MASTER_BAG_DIR)
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
    create_config_file(DEFAULT_TOPIC_CONFIG)
    reader = Ros1BagReader(data_reader_conf_path = TestDataFactory.DEFAULT_CONFIG_PATH,
                           deserialize_raw_data = False,
                           master_file_dir = TestDataFactory.MASTER_BAG_DIR)
    
    with pytest.raises(KeyError):
        loc = RosElementLocation(file = TestDataFactory.FILE1, topic = "/unexist_topic", msgtype="some_msg_type", timestamp = 300)
        request_element_wrong_topic = Element(timestamp=300, measurement = (), location=loc)
        read_element = reader.get_element(request_element_wrong_topic)

    request_element_wrong_timestamp = Element(timestamp=30000, location=RosElementLocation(file = TestDataFactory.FILE1, topic = TestDataFactory.CAMERA_TOPIC, msgtype="some_msg_type", timestamp = 300), measurement = ())
    read_element = reader.get_element(request_element_wrong_timestamp)
    assert read_element == None

    request_element = Element(timestamp=1, location=RosElementLocation(file = TestDataFactory.FILE1, topic = TestDataFactory.IMU_TOPIC, msgtype="some_msg_type", timestamp = 1), measurement = ())
    read_element = reader.get_element(request_element)
    assert read_element.measurement == Measurement(sensor='imu', values=b'123456789ABCDEQGEGKJBNKJBN')

    request_element = Element(timestamp=3, location=RosElementLocation(file = TestDataFactory.FILE1, topic = TestDataFactory.CAMERA_TOPIC, msgtype="some_msg_type", timestamp = 3), measurement = ())
    read_element = reader.get_element(request_element)
    assert read_element.measurement == Measurement(sensor='camera', values=b'JFVNKJGJHK')

    request_element = Element(timestamp=14, location=RosElementLocation(file = TestDataFactory.FILE2, topic = TestDataFactory.GNSS_TOPIC, msgtype="some_msg_type", timestamp = 14), measurement = ())
    read_element = reader.get_element(request_element)
    assert read_element.measurement == Measurement(sensor='gnss', values=b'iubgkhnlkml')

    request_element = Element(timestamp=23, location=RosElementLocation(file = TestDataFactory.FILE3, topic = TestDataFactory.CAMERA_TOPIC, msgtype="some_msg_type", timestamp = 23), measurement = ())
    read_element = reader.get_element(request_element)
    assert read_element.measurement == Measurement(sensor='camera', values=b'KJHKJ')

    request_element = Element(timestamp=8, location=RosElementLocation(file = TestDataFactory.FILE1, topic = TestDataFactory.GNSS_TOPIC, msgtype="some_msg_type", timestamp = 8), measurement = ())
    read_element = reader.get_element(request_element)
    read_element.measurement.values = deserialize_cdr(ros1_to_cdr(read_element.measurement.values, read_element.location.msgtype), read_element.location.msgtype)
    latitude, longitude, altitude = read_element.measurement.values.latitude, read_element.measurement.values.longitude, read_element.measurement.values.altitude
    assert [latitude, longitude, altitude] == TestDataFactory.GNSS_POSITION

def test_close_loop():
    create_config_file(DEFAULT_TOPIC_CONFIG)
    reader = Ros1BagReader(data_reader_conf_path = TestDataFactory.DEFAULT_CONFIG_PATH,
                           deserialize_raw_data = False,
                           master_file_dir = TestDataFactory.MASTER_BAG_DIR,
                           )
    element_cnt = 0
    expected_elements_amount = 20

    while True:
        request_element = Element(timestamp=8, location = RosElementLocation(file = TestDataFactory.FILE1, topic = TestDataFactory.GNSS_TOPIC, msgtype="some_msg_type", timestamp = 8), measurement = ())
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

