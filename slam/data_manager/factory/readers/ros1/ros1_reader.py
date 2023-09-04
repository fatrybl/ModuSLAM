from plum import dispatch
from pathlib import Path
from typing import Iterable, Callable, Optional
import logging

from rosbags.rosbag1 import Reader
from rosbags.serde import deserialize_cdr, ros1_to_cdr
from rosbags.interfaces import Connection

from slam.data_manager.factory.readers.data_reader import DataReader
from slam.data_manager.factory.readers.element_factory import Element, Measurement
from slam.utils.stopping_criterion import StoppingCriterionSingleton
from slam.utils.config import Config
from configs.paths.DEFAULT_FILE_PATHS import RosDataset, ConfigFilePaths


logger = logging.getLogger(__name__)

class Ros1BagReader(DataReader):
    def __init__(self, config_path: Path = ConfigFilePaths.data_reader_config.value,
                       file_name_path: Path = None,
                       raw_data: bool = False):
        super().__init__()

        self.__break_point = StoppingCriterionSingleton()
        
        self.raw_data = raw_data
        if(file_name_path == None):
            self.file = self._dataset_dir / RosDataset.data_stamp.value
        else:
            self.file = file_name_path
        logger.info("Initializing Ros1BagReader: %s\n",self.file.name)
        if (not DataReader.is_file_valid(self.file)):
            logger.critical(
                f"Couldn't initialize the iterator for {self.file}")
            self.__break_point.is_data_processed = True
            raise FileNotFoundError
        
        cfg = Config.from_file(config_path)
        topic_info = cfg.attributes["ros1_reader"]["used_sensors"]
        self.__sensor_info = {k: v for d in topic_info for k, v in d.items()} #keqy - ros topic, value - sensor name
        logger.info("readable topics: %s\n",  self.__sensor_info.keys())
        self.__iterator = self.__init_iterator()
        

    def __init_iterator(self, topic: str = None,  start: Optional[int] = None, stop: Optional[int] = None):
        with Reader(self.file) as reader:
            avilable_topics = set(list(reader.topics.keys()))
            logger.info("available topics ",  avilable_topics)
            # print("available topics ",  avilable_topics)
            # print("required topics ",  self.__sensor_info.keys())
            for topic_name in self.__sensor_info.keys():
                if topic_name not in avilable_topics:
                    logger.critical(f"there are no topic {topic_name} ")
                    raise KeyError
                
                
            if(not topic):
                connections =  ()
            else:
                connections =  reader.topics[topic].connections
            for line in enumerate(reader.messages(connections = connections, start = start, stop = stop)):
                yield line
              
    def __get_next_data(self, iterator) -> tuple:
        while True:
            line = next(iterator)
            ind, (connection, timestamp, rawdata) = line
            if(connection.topic in self.__sensor_info.keys()):
                sensor = self.__sensor_info[connection.topic]
                if(self.raw_data):
                    data = rawdata
                else:
                    data = deserialize_cdr(ros1_to_cdr(rawdata, connection.msgtype), connection.msgtype)
                break
            else:
                logger.info("topic %s is ignored" ,connection.topic)

        location = {"file": self.file,
                    "topic": connection.topic}
        if(self.raw_data):
            location["msgtype"] = connection.msgtype
            
        return sensor, data, timestamp, location

    @dispatch
    def get_element(self, iterator = None)  -> Element | None:
        """
        Gets element from dataset.
        Should be implemented for each reader
        """      
        try:
            if(iterator == None):
                sensor, data, timestamp, location = self.__get_next_data(self.__iterator)
            else:
                sensor, data, timestamp, location = self.__get_next_data(iterator)

            measurement = Measurement(sensor, data)
            return Element(timestamp, measurement, location)

        except StopIteration:
            self.__break_point.is_data_processed = True
            logger.info("data finished")
            return None

    @dispatch
    def get_element(self, element: Element) -> Element:
        timestamp = element.timestamp
        topic = element.location["topic"]
        iterator = self.__init_iterator(topic = topic, start = timestamp, stop = timestamp+1)
        element = self.get_element(iterator)
        if(element == None):
            raise KeyError
        return element

