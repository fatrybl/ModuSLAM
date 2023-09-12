from plum import dispatch
from pathlib import Path
from typing import  Optional
import logging

from rosbags.serde import deserialize_cdr, ros1_to_cdr

from configs.paths.DEFAULT_FILE_PATHS import ConfigFilePaths
from slam.data_manager.factory.readers.data_reader import DataReader
from slam.data_manager.factory.readers.element_factory import Element, Measurement
from slam.utils.config import Config
from slam.data_manager.factory.readers.ros1.dataset_iterator import RosDatasetIterator

logger = logging.getLogger(__name__)


class Ros1BagReader(DataReader):
    def __init__(self, config_path: Path = ConfigFilePaths.data_reader_config.value,
                       master_file_dir: Optional[Path] = None,
                       deserialize_raw_data: bool = False):
        super().__init__()
        self.deserialize_raw_data = deserialize_raw_data
        if(master_file_dir == None):
            master_file_dir = Path(self._dataset_dir)
 
        cfg = Config.from_file(config_path)
        topic_sensor_cfg = cfg.attributes["ros1_reader"]["used_topics"]
        print("--------------------------------")
        print("topic_sensor_cfg",topic_sensor_cfg)
        
        self.__topic_sensor_dict = {k: v for v, k in topic_sensor_cfg.items()} #key - ros topic, value - sensor name
        logger.debug(f"available topics in RosReader: {self.__topic_sensor_dict.keys()}")
        self.__iterator = RosDatasetIterator(master_file_dir = master_file_dir, topics = self.__topic_sensor_dict.keys())
              
    def __get_next_element(self, iterator) -> Element | None:
        while True:
            try:
                line = next(iterator)
            except StopIteration:
                 logger.info("data finished")
                 return None
            file, topic, msgtype, timestamp, rawdata = line
            if(topic in self.__topic_sensor_dict.keys()):
                sensor = self.__topic_sensor_dict[topic]
                if(self.deserialize_raw_data):
                    data = deserialize_cdr(ros1_to_cdr(rawdata, msgtype), msgtype)
                else:
                    data = rawdata
                break

        location = {"file": file,
                    "topic": topic}
        if(not self.deserialize_raw_data):
            location["msgtype"] = msgtype

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
        timestamp = element.timestamp
        file = element.location["file"]
        topics = [element.location["topic"]]
        iterator = self.__iterator.get_iterator(file = file, topics = topics, start = timestamp, stop = timestamp+1)
        element = self.__get_next_element(iterator)
        if(element is None):
            logger.critical("no element with such location")
        return element

