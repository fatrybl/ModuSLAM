from plum import dispatch
from pathlib import Path
from typing import  Optional
import logging

from rosbags.serde import deserialize_cdr, ros1_to_cdr

from configs.paths.DEFAULT_FILE_PATHS import ConfigFilePaths
from slam.data_manager.factory.readers.data_reader import DataReader
from slam.data_manager.factory.readers.element_factory import Element, Measurement
from slam.utils.stopping_criterion import StoppingCriterionSingleton
from slam.utils.config import Config
from slam.data_manager.factory.readers.ros1.dataset_iterator import RosDatasetIterator

logger = logging.getLogger(__name__)


class Ros1BagReader(DataReader):
    def __init__(self, config_path: Path = ConfigFilePaths.data_reader_config.value,
                       master_file_path: Optional[Path] = None,
                       deserialize_raw_data: bool = False):
        super().__init__()
        self.__break_point = StoppingCriterionSingleton()
        self.deserialize_raw_data = deserialize_raw_data
        
        if(master_file_path == None):
            master_file_path = Path(self._dataset_dir)
 
        cfg = Config.from_file(config_path)
        topic_info = cfg.attributes["ros1_reader"]["used_sensors"]
        self.__sensor_info = {k: v for d in topic_info for v, k in d.items()} #key - ros topic, value - sensor name
        logger.info(f"readable topics: {self.__sensor_info.keys()}")
        self.__iterator = RosDatasetIterator(master_file_path = master_file_path, topics = self.__sensor_info.keys())
              
    def __get_next_data(self, iterator) -> tuple:
        while True:
            line = next(iterator)
            file, topic, msgtype, timestamp, rawdata = line
            if(topic in self.__sensor_info.keys()):
                sensor = self.__sensor_info[topic]
                if(self.deserialize_raw_data):
                    data = deserialize_cdr(ros1_to_cdr(rawdata, msgtype), msgtype)
                else:
                    data = rawdata
                break
            else:
                logger.info(f"topic {topic} is ignored")

        location = {"file": file,
                    "topic": topic}
        if(not self.deserialize_raw_data):
            location["msgtype"] = msgtype
        return sensor, data, timestamp, location

    @dispatch
    def get_element(self)  -> Element | None:
        """
        Concurrently gets elements from dataset.
        """      
        try:
            sensor, data, timestamp, location = self.__get_next_data(self.__iterator)
            measurement = Measurement(sensor, data)
            return Element(timestamp, measurement, location)
        except StopIteration:
            logger.info("data finished")
            self.__break_point.is_data_processed = True
            return None

    @dispatch
    def get_element(self, element: Element) -> Element | None:
        """
        Gets elements from dataset with given location.
        """  
        timestamp = element.timestamp
        file = element.location["file"]
        topics = [element.location["topic"]]
        iterator = self.__iterator.get_iterator(file = file, topics = topics, start = timestamp, stop = timestamp+1)
        try:
            sensor, data, timestamp, location = self.__get_next_data(iterator)
            measurement = Measurement(sensor, data)
            return Element(timestamp, measurement, location)
        except StopIteration:
            logger.critical("no element with such location")
            return None

