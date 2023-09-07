import pytest
from pathlib import Path

from rosbags.rosbag1 import Writer

from slam.data_manager.factory.readers.ros1.ros1_reader import Ros1BagReader
from slam.data_manager.factory.readers.element_factory import Element, Measurement
from tests.data_manager.Ros1Reader.conftest import TEST_BAG_PATH, DEFAULT_CONFIG_PATH, create_config_file



def test_unknown_file_scenario():
    path = Path(__file__).parent/ "non_exist.bag" 
    with pytest.raises(FileNotFoundError):
        reader = Ros1BagReader(file_name_path = path)
        reader.get_element()



def test_unknown_topic_scenario():
    create_config_file({"ros1_reader": {"used_sensors": [{"/imu_topic": "imu"},
                                                         {"/unknown_topic": "camera"},
                                                        ]
                                        }
                          })
    with pytest.raises(KeyError):
        reader = Ros1BagReader(config_path = DEFAULT_CONFIG_PATH,
                            file_name_path = TEST_BAG_PATH,
                            raw_data= True)
        reader.get_element()



scenario_all_topics = ({"ros1_reader": {"used_sensors": [{"imu": "/imu_topic"},
                                                        {"camera": "/camera_topic"},
                                                        {"lidar": "/lidar_topic"},
                                                        {"gnss": "/gnss_topic"}]
                                 }
                       }, 8)


scenario_half_topics = ({"ros1_reader": {"used_sensors": [{"imu": "/imu_topic"},
                                                          {"camera": "/camera_topic"},
                                                  ]
                                 }
                 }, 4)
success_scenarios = [scenario_all_topics, scenario_half_topics]

@pytest.mark.parametrize(
    ("test_cfg", "expected_element_cnt"), success_scenarios
)
def test_ros_elements_amount(test_cfg: dict[str, dict[str, str]], expected_element_cnt):
    create_config_file(test_cfg)
    reader = Ros1BagReader(config_path = DEFAULT_CONFIG_PATH,
                           file_name_path = TEST_BAG_PATH,
                           raw_data= True)
    element_cnt = 0
    while True:
        element = reader.get_element()
        if(element == None):
            break
        element_cnt+=1
    assert element_cnt == expected_element_cnt



def test_ros_get_element():
    create_config_file({"ros1_reader": {"used_sensors": [{"imu": "/imu_topic"},
                                                        {"camera": "/camera_topic"},
                                                        {"lidar": "/lidar_topic"},
                                                        {"gnss": "/gnss_topic"}]
                                 }
                       })
    reader = Ros1BagReader(config_path = DEFAULT_CONFIG_PATH,
                           file_name_path = TEST_BAG_PATH,
                           raw_data= True)
    
    with pytest.raises(KeyError):
        request_element_wrong_topic = Element(timestamp=300, location={"topic": "/unexist_topic"}, measurement = ())
        read_element = reader.get_element(request_element_wrong_topic)


    request_element_wrond_timestamp = Element(timestamp=30000, location={"topic": "/camera_topic"}, measurement = ())
    read_element = reader.get_element(request_element_wrond_timestamp)
    assert read_element == None

    request_element = Element(timestamp=1, location={"topic": "/imu_topic"}, measurement = ())
    read_element = reader.get_element(request_element)
    assert read_element.measurement == Measurement(sensor='imu', values=b'123456789ABCDEQGEGKJBNKJBN')
    request_element = Element(timestamp=8, location={"topic": "/gnss_topic"}, measurement = ())
    read_element = reader.get_element(request_element)
    assert read_element.measurement == Measurement(sensor='gnss', values=b'kjnk987')
    request_element = Element(timestamp=3, location={"topic": "/camera_topic"}, measurement = ())
    read_element = reader.get_element(request_element)
    assert read_element.measurement == Measurement(sensor='camera', values=b'JFVNKJGJHK')
    request_element = Element(timestamp=2, location={"topic": "/lidar_topic"}, measurement = ())
    read_element = reader.get_element(request_element)
    assert read_element.measurement == Measurement(sensor='lidar', values=b'DEADSFEEF')