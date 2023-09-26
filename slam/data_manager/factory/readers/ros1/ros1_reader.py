import logging
from plum import dispatch
from pathlib import Path
from typing import  Optional
from typing import Type
from dataclasses import dataclass

from rosbags.serde import deserialize_cdr, ros1_to_cdr

from slam.data_manager.factory.readers.data_reader import DataReader
from slam.data_manager.factory.readers.element_factory import Element, Measurement
from slam.data_manager.factory.readers.ros1.dataset_iterator import RosManager, RosDatasetIterator, RosFileRangeLocation, RosElementLocation
from slam.utils.exceptions import NotSubset
from slam.setup_manager.sensor_factory.sensor_factory import SensorFactory
from slam.setup_manager.sensor_factory.sensors import Sensor

@dataclass
class RosConfig():
    topic_sensor_cfg: dict[str, str] #key is sensor name value is topic name
    sensors: list[str]
    master_file_dir: Path
    deserialize_raw_data: bool

logger = logging.getLogger(__name__)


class Ros1BagReader(DataReader):
    def __init__(self, cfg : RosConfig):
        super().__init__()
        self.deserialize_raw_data = cfg.deserialize_raw_data
        used_sensors: set[str] = set(cfg.sensors)
        self.__topic_sensor_dict = dict()
        for sensor in used_sensors:
            if(sensor not in cfg.topic_sensor_cfg):
                logger.critical(f"no topic info for {sensor}, available sensors are {used_sensors}")
                raise NotSubset
            topic: str = cfg.topic_sensor_cfg[sensor]
            self.__topic_sensor_dict[topic] = sensor

        logger.debug(f"available topics in RosReader: {self.__topic_sensor_dict.keys()}")
        self.__sensor_factory = SensorFactory()
        self.__ros_manager = RosManager(master_file_dir = cfg.master_file_dir, topics = self.__topic_sensor_dict.keys())
        self.__dataset_iterator: RosDatasetIterator = self.__ros_manager.get_main_iterator()

    def __get_next_element(self, iterator: RosDatasetIterator) -> Element | None:
        while True:
            try:
                location : RosElementLocation
                rawdata  : bytes
                location, rawdata = next(iterator)
            except StopIteration:
                 logger.info("data finished")
                 return None
            topic: str = location.topic
            timestamp: int = location.timestamp
            if(topic in self.__topic_sensor_dict.keys()):
                sensor_name: str = self.__topic_sensor_dict[topic]
                sensor: Type[Sensor] = self.__sensor_factory.name_to_sensor(sensor_name)
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
        return self.__get_next_element(self.__dataset_iterator)


    @dispatch
    def get_element(self, element: Element) -> Element | None:
        """Gets element from dataset with given location.
        Args:
            element (Element): 

        Returns:
            Element | None if we reach end of dataset
        """
        location = RosFileRangeLocation(topics=[element.location.topic], start = element.location.timestamp, stop = element.location.timestamp+1)
        iterator = self.__ros_manager.get_iterator_from_file(file = element.location.file, location = location)
        element = self.__get_next_element(iterator)
        if(element is None):
            logger.critical("no element with such location")
        return element


    def get_elements(self, t1: int, t2: int) -> list[Element]:
        """get elements from given locations

        Args:
            t1 (int): start time
            t2 (int): end time

        Returns:
            list[Element]: list of elements
        """
        location = RosFileRangeLocation(topics=None, start = t1, stop = t2+1)
        iterator = self.__ros_manager.get_iterator(location = location)
        element_list = []
        while(1):
            element = self.__get_next_element(iterator)
            if(element is None):
                break
            element_list.append(element)
        if(len(element_list) == 0):
            logger.critical(f"get_elements: empty list for timestamp {t1} : {t2}")
        return element_list