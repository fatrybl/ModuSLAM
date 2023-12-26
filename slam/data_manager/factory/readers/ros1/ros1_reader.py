import logging
from plum import dispatch
from typing import Type
from pathlib import Path
from typing import  Optional
from rosbags.serde import deserialize_cdr, ros1_to_cdr

from slam.data_manager.factory.readers.data_reader import DataReader
from slam.data_manager.factory.readers.element_factory import Element, Measurement
from slam.data_manager.factory.readers.ros1.dataset_iterator import  RosDatasetIterator, RosDataRange, RosElementLocation
from slam.data_manager.factory.readers.ros1.ros_manager import RosManager
from slam.setup_manager.sensor_factory.sensors import Sensor
from slam.setup_manager.sensor_factory.sensor_factory import SensorFactory
from slam.utils.auxiliary_dataclasses import TimeRange
from configs.experiments.ros1.config import  RosSensorConfig

from configs.system.data_manager.regime import Regime, TimeLimit
from configs.system.data_manager.datasets.ros1 import Ros1

from slam.setup_manager.sensor_factory.sensors import (
    Sensor, Imu, Fog, Encoder, StereoCamera, Altimeter, Gps, VrsGps, Lidar2D, Lidar3D)
logger = logging.getLogger(__name__)


class Ros1BagReader(DataReader):
    def __init__(self, cfg : Ros1, regime_params: type[Regime]):
        super().__init__()
        self.deserialize_raw_data: bool = cfg.deserialize_raw_data
        used_sensors_info: list[RosSensorConfig] = cfg.used_sensors
        self.__topic_sensor_dict: dict[str, Sensor] = dict()
        self.__sensor_topic_dict: dict[str, str] = dict()
        for sensor_cfg in used_sensors_info:
            sensor: Type[Sensor] = sensor_cfg.sensor
            topic: str = sensor_cfg.topic
            self.__topic_sensor_dict[topic] = sensor
            self.__sensor_topic_dict[sensor.name] = topic
        msg = f"available topics in RosReader: {self.__topic_sensor_dict.keys()}"  
        logger.debug(msg)
        master_file_dir: Path = Path(cfg.directory)
        self.__ros_manager = RosManager(master_file_dir = master_file_dir, topics = self.__topic_sensor_dict.keys())

        data_range = RosDataRange()
        if regime_params.name == TimeLimit.__name__:
            data_range.start = regime_params.start
            data_range.stop = regime_params.stop

        self.__main_dataset_iterator: RosDatasetIterator = self.__ros_manager.get_iterator(data_range)
  
    def __get_next_element(self, iterator: RosDatasetIterator) -> Element | None:
        while True:
            try:
                location : RosElementLocation
                timestamp : int
                rawdata  : bytes
                location, timestamp, rawdata = next(iterator)
            except StopIteration:
                 logger.info("data finished")
                 return None
            topic: str = location.topic
            if(topic in self.__topic_sensor_dict.keys()):
                sensor: Type[Sensor]  = self.__topic_sensor_dict[topic]
                if(self.deserialize_raw_data):
                    msgtype = location.msgtype
                    data = deserialize_cdr(ros1_to_cdr(rawdata, msgtype), msgtype)
                else:
                    data = rawdata
                break
        measurement = Measurement(sensor, (data))
        return Element(timestamp, measurement, location)

    @dispatch
    def get_element(self)  -> Element | None:
        """get element from dataset concurently

        Returns:
            Element 
            None if we reach end of dataset
        """
        return self.__get_next_element(self.__main_dataset_iterator)


    @dispatch
    def get_element(self, element_no_data: Element) -> Element | None:
        """Gets element from dataset with given location.
        Args:
            element (Element): 

        Returns:
            Element | None if we reach end of dataset
        """
        data_range = RosDataRange(topics=[element_no_data.location.topic], start = element_no_data.timestamp, stop = element_no_data.timestamp+1)
        iterator: RosDatasetIterator = self.__ros_manager.get_iterator(element_no_data.location.file, data_range)
        element_with_data = self.__get_next_element(iterator)
        if(element_with_data is None):
            logger.critical("no element with such location")
        return element_with_data


    @dispatch
    def get_element(self, q1: int, timestamp: int | None = None) -> None:
        """get elements from given locations

        Args:
            time_range (SensorData): sensor time
        Returns:
            list[Element]: list of elements
        """
        print("here  I am")
 
    
    @dispatch
    def get_element(self, sensor: Sensor, timestamp: int | None = None) -> Element:
        """get elements from given locations

        Args:
            time_range (SensorData): sensor time
        Returns:
            list[Element]: list of elements
        """
        #print("here  I am")
        if(timestamp):
            topic: str = self.__sensor_topic_dict[sensor.name]
            data_range = RosDataRange(topics=[topic], start = timestamp)
            self.__temp_dataset_iterator: RosDatasetIterator = self.__ros_manager.get_iterator(data_range)

        return self.__get_next_element(self.__temp_dataset_iterator)