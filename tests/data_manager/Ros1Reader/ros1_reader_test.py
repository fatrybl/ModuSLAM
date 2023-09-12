import pytest
from pathlib import Path

from rosbags.serde import deserialize_cdr, ros1_to_cdr

from slam.data_manager.factory.readers.ros1.ros1_reader import Ros1BagReader
from slam.data_manager.factory.readers.element_factory import Element, Measurement
from tests.data_manager.Ros1Reader.data_factory import TestDataFactory, create_config_file


def test_unknown_file_scenario():
    create_config_file({"ros1_reader": {"used_sensors": [{"/imu_topic": "imu"},
                                                        {"/camera_topic": "camera"},
                                                    ]
                                    }
                        })
    path = Path(__file__).parent/ "non_exist.bag" 
    with pytest.raises(FileNotFoundError):
        reader = Ros1BagReader(master_file_dir = path)
        reader.get_element()



def test_unknown_topic_scenario():
    create_config_file({"ros1_reader": {"used_sensors": [{"/imu_topic": "imu"},
                                                         {"/unknown_topic": "camera"},
                                                        ]
                                        }
                          })
    with pytest.raises(KeyError):
        reader = Ros1BagReader(config_path = TestDataFactory.DEFAULT_CONFIG_PATH,
                            master_file_dir = TestDataFactory.MASTER_BAG_DIR,
                            deserialize_raw_data = False)



scenario_all_topics = ({"ros1_reader": {"used_sensors": [{"imu": "/imu_topic"},
                                                        {"camera": "/camera_topic"},
                                                        {"lidar": "/lidar_topic"},
                                                        {"gnss": "/gnss_topic"}]
                                 }
                       }, 20)


scenario_half_topics = ({"ros1_reader": {"used_sensors": [{"imu": "/imu_topic"},
                                                          {"camera": "/camera_topic"},
                                                  ]
                                 }
                 }, 10)
success_scenarios = [scenario_all_topics, scenario_half_topics]

@pytest.mark.parametrize(
    ("test_cfg", "expected_element_cnt"), success_scenarios
)
def test_ros_elements_amount(test_cfg: dict[str, dict[str, str]], expected_element_cnt):
    create_config_file(test_cfg)
    reader = Ros1BagReader(config_path = TestDataFactory.DEFAULT_CONFIG_PATH,
                           master_file_dir = TestDataFactory.MASTER_BAG_DIR,
                           deserialize_raw_data = False)
    element_cnt = 0
    while True:
        element = reader.get_element()
        if(element == None):
            break
        element_cnt+=1
    assert element_cnt == expected_element_cnt



def test_ros_get_element():
    create_config_file()
    reader = Ros1BagReader(config_path = TestDataFactory.DEFAULT_CONFIG_PATH,
                           master_file_dir = TestDataFactory.MASTER_BAG_DIR,
                           deserialize_raw_data= False)
    
    with pytest.raises(KeyError):
        request_element_wrong_topic = Element(timestamp=300, location={"file": TestDataFactory.FILE1,"topic": "/unexist_topic"}, measurement = ())
        read_element = reader.get_element(request_element_wrong_topic)


    request_element_wrond_timestamp = Element(timestamp=30000, location={"file": TestDataFactory.FILE1, "topic": "/camera_topic"}, measurement = ())
    read_element = reader.get_element(request_element_wrond_timestamp)
    assert read_element == None

    request_element = Element(timestamp=1, location={"file": TestDataFactory.FILE1, "topic": "/imu_topic"}, measurement = ())
    read_element = reader.get_element(request_element)
    assert read_element.measurement == Measurement(sensor='imu', values=b'123456789ABCDEQGEGKJBNKJBN')

    request_element = Element(timestamp=3, location={"file": TestDataFactory.FILE1, "topic": "/camera_topic"}, measurement = ())
    read_element = reader.get_element(request_element)
    assert read_element.measurement == Measurement(sensor='camera', values=b'JFVNKJGJHK')

    request_element = Element(timestamp=14, location={"file": TestDataFactory.FILE2, "topic": "/gnss_topic"}, measurement = ())
    read_element = reader.get_element(request_element)
    assert read_element.measurement == Measurement(sensor='gnss', values=b'iubgkhnlkml')

    request_element = Element(timestamp=23, location={"file": TestDataFactory.FILE3, "topic": "/camera_topic"}, measurement = ())
    read_element = reader.get_element(request_element)
    assert read_element.measurement == Measurement(sensor='camera', values=b'KJHKJ')

    request_element = Element(timestamp=8, location={"file": TestDataFactory.FILE1, "topic": "/gnss_topic"}, measurement = ())
    read_element = reader.get_element(request_element)
    read_element.measurement.values = deserialize_cdr(ros1_to_cdr(read_element.measurement.values, read_element.location["msgtype"]), read_element.location["msgtype"])
    latitude, longitude, altitude = read_element.measurement.values.latitude, read_element.measurement.values.longitude, read_element.measurement.values.altitude
    assert latitude == 1.0
    assert longitude == 2.0
    assert altitude == 3.0
    
def test_ros_get_element_in_middle():
    create_config_file()
    reader = Ros1BagReader(config_path = TestDataFactory.DEFAULT_CONFIG_PATH,
                           master_file_dir = TestDataFactory.MASTER_BAG_DIR,
                           deserialize_raw_data= False)
    element_cnt = 0
    for i in range(7):
        element = reader.get_element()
        element_cnt+=1
    request_element = Element(timestamp=8, location={"file": TestDataFactory.FILE1, "topic": "/gnss_topic"}, measurement = ())
    read_element = reader.get_element(request_element)
    read_element.measurement.values = deserialize_cdr(ros1_to_cdr(read_element.measurement.values, read_element.location["msgtype"]), read_element.location["msgtype"])
    latitude, longitude, altitude = read_element.measurement.values.latitude, read_element.measurement.values.longitude, read_element.measurement.values.altitude
    assert latitude == 1.0
    assert longitude == 2.0
    assert altitude == 3.0
    while True:
        element = reader.get_element()
        if(element == None):
            break
        element_cnt+=1
    assert element_cnt == 20

