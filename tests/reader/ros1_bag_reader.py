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



DEFAULT_CONFIG_PATH = Path(__file__).parent / "data_manager.yaml"


class ConfigEnum(Enum):
    config_path = DEFAULT_CONFIG_PATH


def create_config_file(cfg: dict) -> None:
    with open(DEFAULT_CONFIG_PATH, 'w') as outfile:
        dump(cfg, outfile)

def create_config_file(cfg: dict) -> None:
    with open(DEFAULT_CONFIG_PATH, 'w') as outfile:
        dump(cfg, outfile)


scenario_ros1 = ({"data": {"dataset_type": "ros1",
                       "dataset_directory": "/home/ilia/mySLAM/data/rosbag/0-Tiltlaser.bag"}})
success_scenarios = [scenario_ros1]

@pytest.mark.parametrize(
    ("test_cfg"), success_scenarios
)
def test_ros_reader(test_cfg: dict[str, dict[str, str]]):
    create_config_file(test_cfg)

    for N in [1, 10, 20]:   
        reader = DataReaderFactory(ConfigEnum.config_path.value)
        new_element: Element
        for i in range(N):
            element = reader.get_element()
            if(element == None):
                break
            else:
                new_element = element

        measurements =  { "location": new_element.location,   
                        "timestamp": new_element.timestamp}
        element = reader.get_element_with_measurement(measurements)
        # print(element.measurement.values)
        # print(new_element.measurement)
        assert element.timestamp == new_element.timestamp
        assert element.location == new_element.location
        assert element.measurement.values.header == new_element.measurement.values.header


scenario_ros1 = ({"data": {"dataset_type": "ros1",
                          "dataset_directory": "/home/ilia/mySLAM/data/rosbag/0-Tiltlaser.bag"}})
success_scenarios = [scenario_ros1]
@pytest.mark.parametrize(
    ("test_cfg"), success_scenarios
)
def test_ros1_reader(test_cfg: dict[str, dict[str, str]]):
    pass
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