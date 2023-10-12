import logging
from plum import dispatch
from typing import Type

from rosbags.serde import deserialize_cdr, ros1_to_cdr

from slam.data_manager.factory.readers.data_reader import DataReader
from slam.data_manager.factory.readers.element_factory import Element, Measurement
from slam.data_manager.factory.readers.ros1.dataset_iterator import  RosDatasetIterator, RosDataRange, RosElementLocation
from slam.data_manager.factory.readers.ros1.ros_manager import RosManager
from slam.setup_manager.sensor_factory.sensors import Sensor
from slam.setup_manager.sensor_factory.sensor_factory import SensorFactory
from configs.experiments.ros1.config import Ros1, SensorConfig
from slam.utils.auxiliary_dataclasses import TimeRange

logger = logging.getLogger(__name__)


class Ros1BagReader(DataReader):
    def __init__(self, cfg : Ros1):
        super().__init__()

        self.deserialize_raw_data = cfg.data_manager.dataset.deserialize_raw_data
        used_sensors:list[SensorConfig] = cfg.setup_manager.used_sensors
        self.__topic_sensor_dict: dict[str, Sensor] = dict()
        self.__sensor_topic_dict: dict[str, str] = dict()
        for sensor_cfg in used_sensors:
            sensor: Type[Sensor] = SensorFactory.name_to_sensor(sensor_cfg.name)
            topic: str = sensor_cfg.topic
            self.__topic_sensor_dict[topic] = sensor
            self.__sensor_topic_dict[sensor_cfg.type] = topic
        msg = f"available topics in RosReader: {self.__topic_sensor_dict.keys()}"  
        logger.debug(msg)
        self.__ros_manager = RosManager(master_file_dir = cfg.data_manager.dataset.directory, topics = self.__topic_sensor_dict.keys())
        self.__main_dataset_iterator: RosDatasetIterator = self.__ros_manager.get_iterator()
  
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
        measurement = Measurement(sensor, data)
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
    def get_element(self, time_range : TimeRange, sensor_name: str, first_element: bool = False) -> Element | None:
        """get elements from given locations

        Args:
            time_range (SensorData): sensor time
        Returns:
            list[Element]: list of elements
        """
        if(first_element):
            topic: str = self.__sensor_topic_dict[sensor_name]
            data_range = RosDataRange(topics=[topic], start = time_range.start, stop = time_range.stop + 1)
            self.__temp_dataset_iterator: RosDatasetIterator = self.__ros_manager.get_iterator(data_range)

        return self.__get_next_element(self.__temp_dataset_iterator)