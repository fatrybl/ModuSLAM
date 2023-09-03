import pytest
from yaml import dump
from enum import Enum
from pathlib import Path
import numpy as np
from slam.data_manager.factory.readers.data_reader import DataReader
from slam.data_manager.factory.readers.kaist.kaist_reader import KaistReader
from slam.data_manager.factory.readers.ros1.ros1_reader import Ros1BagReader
from rosbags.rosbag1 import Writer
from slam.data_manager.factory.readers.data_reader_factory import DataReaderFactory
from slam.data_manager.factory.readers.element_factory import Element



DEFAULT_CONFIG_PATH = Path(__file__).parent / "data_readers.yaml"



class ConfigEnum(Enum):
    config_path = DEFAULT_CONFIG_PATH


def create_config_file(cfg: dict) -> None:
    with open(DEFAULT_CONFIG_PATH, 'w') as outfile:
        dump(cfg, outfile)

def create_test_bag(path: Path):
    if (DataReader.is_file_valid(path)):
        path.unlink()
    with Writer(path) as writer:
        conn_imu = writer.add_connection('/imu_topic', 'sensor_msgs/msg/Imu', 'MESSAGE_DEFINITION')
        conn_camera = writer.add_connection('/camera_topic', 'sensor_msgs/msg/Image', 'MESSAGE_DEFINITION')
        conn_lidar = writer.add_connection('/lidar_topic', 'sensor_msgs/msg/LaserScan', 'MESSAGE_DEFINITION')
        conn_gnss = writer.add_connection('/gnss_topic', 'sensor_msgs/msg/NavSatFix', 'MESSAGE_DEFINITION')
        
        writer.write(conn_imu, 1, b'123456789ABCDEQGEGKJBNKJBN')
        writer.write(conn_lidar, 2, b'DEADSFEEF')
        writer.write(conn_camera, 3, b'LKMLK2')
        writer.write(conn_gnss, 4, b'kjnk987')
        writer.write(conn_imu, 4, b'LKMLK2')
        writer.write(conn_lidar, 5, b'LKMLK2')
        writer.write(conn_camera, 6, b'12345')
        writer.write(conn_gnss, 8, b'kjnk987')
        
# scenario_ros1 = ({"ros1_reader": {"used_sensors": [{"/imu_data": "imu"},
#                                                  {"/position_gps": "gps"},
#                                                  {"/scan": "lidar"}]
#                                  }
#                  })

# success_scenarios = [scenario_ros1]

# @pytest.mark.parametrize(
#     ("test_cfg"), success_scenarios
# )
# def test_ros_reader(test_cfg: dict[str, dict[str, str]]):
#     create_config_file(test_cfg)
#     for N in [1, 10, 20]:   
#         reader = Ros1BagReader(config_path = ConfigEnum.config_path.value)
#         #reader = Ros1BagReader()
#         new_element: Element
#         for i in range(N):
#             element = reader.get_element()
#             if(element == None):
#                 break
#             else:
#                 new_element = element

#         measurements =  { "location": new_element.location,   
#                         "timestamp": new_element.timestamp}
#         element = reader.get_element_with_measurement(measurements)
#         # print(element.measurement.values)
#         # print(new_element.measurement)
#         assert element.timestamp == new_element.timestamp
#         assert element.location == new_element.location
#         assert element.measurement.values.header == new_element.measurement.values.header



scenario_ros1 = ({"ros1_reader": {"used_sensors": [{"/imu_topic": "imu"},
                                                   {"/camera_topic": "camera"},
                                                   {"/lidar_topic": "lidar"},
                                                   {"/gnss_topic": "gnss"}]
                                 }
                 }, 8)


scenario_ros2 = ({"ros1_reader": {"used_sensors": [{"/imu_topic": "imu"},
                                                   {"/camera_topic": "camera"},
                                                  ]
                                 }
                 }, 4)
success_scenarios = [scenario_ros1, scenario_ros2]

@pytest.mark.parametrize(
    ("test_cfg", "expected_output"), success_scenarios
)
def test_ros1_reader(test_cfg: dict[str, dict[str, str]], expected_output):
    create_config_file(test_cfg)
    path = Path(__file__).parent/ "test10.bag" 
    create_test_bag(path)
    reader = Ros1BagReader(config_path = ConfigEnum.config_path.value,
                           file_name_path = path,
                           raw_data= True)
    i = 0
    while True:
        element = reader.get_element()
        if(element == None):
            break
        i+=1
        #print(element)
    assert i == expected_output
    path.unlink()



unknown_topic_scenario = [({"ros1_reader": {"used_sensors": [{"/imu_topic": "imu"},
                                                   {"/unknown_topic": "camera"},
                                                  ]
                                 }
                 }, KeyError)]

@pytest.mark.parametrize(
    ("test_cfg", "expected_output"), unknown_topic_scenario
)
def test_unknown_topic_scenario(test_cfg, expected_output):
    create_config_file(test_cfg)
    path = Path(__file__).parent/ "test10.bag" 
    create_test_bag(path)
    with pytest.raises(expected_output):
        reader = Ros1BagReader(config_path = ConfigEnum.config_path.value,
                            file_name_path = path,
                            raw_data= True)
        reader.get_element()
        path.unlink()


unknown_file_scenario = [ ({"ros1_reader": {"used_sensors": [{"/imu_topic": "imu"},
                                                   {"/camera_topic": "camera"},
                                                  ]
                                 }
                 }, ValueError)]

@pytest.mark.parametrize(
    ("test_cfg", "expected_output"), unknown_file_scenario
)
def test_unknown_file_scenario(test_cfg, expected_output):
    create_config_file(test_cfg)
    path = Path(__file__).parent/ "non_exist__.bag" 
    with pytest.raises(expected_output):
        reader = Ros1BagReader(config_path = ConfigEnum.config_path.value,
                            file_name_path = path,
                            raw_data= True)
        reader.get_element()

    # while True:
    #     element = reader.get_element()
    #     if(element == None):
    #         break
    #     i+=1
    #     print(element)

# scenario_ros_bad = ({"data": {"dataset_type": "ros1",
#                        "dataset_directory": "/home/ilia/mySLAM/data/rosbag/unknown.bag"}})
# def test_bad_reader(test_cfg):
#     create_config_file(test_cfg)
#     try:
#         reader = DataReaderFactory(ConfigEnum.config_path.value)
#         new_element: Element
#         N = 30
#         for i in range(N):
#             element_bd = reader.get_element()
#             if(element_bd == None):
#                 break
#             else:
#                 new_element = element_bd

#         measurements =  { "location": new_element.location,   
#                          "timestamp": new_element.timestamp}
#         element = reader.get_element_with_measurement(measurements)
#         # print(element.measurement.values)
#         # print(new_element.measurement)
#         assert element.timestamp == new_element.timestamp
#         assert element.location == new_element.location
#         assert element.measurement.values.header == new_element.measurement.values.header
#     except Exception as e:
#         print(e)
#         raise Exception