import logging
from plum import dispatch
from pathlib import Path
from typing import  Optional
from collections.abc import Iterator
from dataclasses import dataclass, field

from rosbags.serde import deserialize_cdr, ros1_to_cdr

from configs.paths.DEFAULT_FILE_PATHS import ConfigFilePaths
from slam.data_manager.factory.readers.data_reader import DataReader
from slam.data_manager.factory.readers.element_factory import Element, Measurement
from slam.utils.config import Config
from slam.data_manager.factory.readers.ros1.dataset_iterator import RosDatasetIterator, RosFileRangeLocation
from slam.utils.sensor_factory.sensors_factory import SensorFactory
from slam.utils.sensor_factory.sensors import Sensor
from slam.utils.exceptions import NotSubset
logger = logging.getLogger(__name__)


class Ros1BagReader(DataReader):
    def __init__(self, config_path: Path = ConfigFilePaths.data_reader_config.value,
                       deserialize_raw_data: bool = False,
                       master_file_dir: Optional[Path] = None):
        super().__init__()
        self.deserialize_raw_data = deserialize_raw_data
        if(master_file_dir == None):
            config = Config.from_file(ConfigFilePaths.data_manager_config.value)
            master_file_dir = Path(config.attributes["data"]["dataset_directory"])

        cfg: Config = Config.from_file(config_path)

        self.__used_sensors: set[str] = set(cfg.attributes["used_sensors"])
        topic_sensor_cfg = cfg.attributes["ros1_reader"]["used_topics"]
        self.__topic_sensor_dict = dict()
        for sensor in self.__used_sensors:
            if(sensor not in topic_sensor_cfg):
                logger.critical(f"no topic for  {sensor} in config, available sensors are {topic_sensor_cfg}")
                raise NotSubset
            topic = topic_sensor_cfg[sensor]
            self.__topic_sensor_dict[topic] = sensor

        logger.debug(f"available topics in RosReader: {self.__topic_sensor_dict.keys()}")

        self.__iterator = RosDatasetIterator(master_file_dir = master_file_dir, topics = self.__topic_sensor_dict.keys())
              
    def __get_next_element(self, iterator) -> Element | None:
        while True:
            try:
                location, rawdata = next(iterator)
            except StopIteration:
                 logger.info("data finished")
                 return None
            topic: str = location.topic
            timestamp: int = location.timestamp
            if(topic in self.__topic_sensor_dict.keys()):
                sensor = self.__topic_sensor_dict[topic]
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
        """
        Concurrently gets elements from dataset.
        """      
        return self.__get_next_element(self.__iterator)


    @dispatch
    def get_element(self, element: Element) -> Element | None:
        """
        Gets elements from dataset with given location.
        """  
        location = RosFileRangeLocation(topics=[element.location.topic], start = element.location.timestamp, stop = element.location.timestamp+1)
        iterator = self.__iterator.get_iterator(file = element.location.file, location = location)
        element = self.__get_next_element(iterator)
        if(element is None):
            logger.critical("no element with such location")
        return element

