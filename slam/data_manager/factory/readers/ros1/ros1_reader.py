from plum import dispatch
from pathlib import Path
from typing import  Optional, Iterable
import logging

from rosbags.rosbag1 import Reader
from rosbags.serde import deserialize_cdr, ros1_to_cdr

from configs.paths.DEFAULT_FILE_PATHS import RosDataset, ConfigFilePaths
from slam.data_manager.factory.readers.data_reader import DataReader
from slam.data_manager.factory.readers.element_factory import Element, Measurement
from slam.utils.stopping_criterion import StoppingCriterionSingleton
from slam.utils.config import Config



logger = logging.getLogger(__name__)

class RosFileStorage():
    def __init__(self, file: Path):
        self.file = file
        self.__reader = Reader(file)
        self.__reader.open()
        if(self.__reader.message_count == 0):
            raise ValueError
        self.__avilable_topics = set(list(self.__reader.topics.keys()))
        logger.info(f"available topics {self.__avilable_topics}")
        
    def check_correct_topic(self, topics: Iterable[str]):
        for topic_name in topics:
            if topic_name not in self.__avilable_topics:
                logger.critical(f"there are no topic {topic_name} ")
                raise KeyError
            
    def get_iterator(self, topics: Iterable[str],  start: Optional[int] = None, stop: Optional[int] = None):
        self.check_correct_topic(topics)
        connections = []
        for topic in topics:
            connections.append(*self.__reader.topics[topic].connections)
        for line in self.__reader.messages(connections = connections, start = start, stop = stop):
            connection, timestamp, rawdata = line
            yield self.file, connection.topic, connection.msgtype, timestamp, rawdata

    def __exit__(self):
        self.__reader.close()
        
class RosDatasetIterator():
    def __init__(self, master_file_path:Path, topics: Iterable[str]):
        file_data_dir = master_file_path/RosDataset.data_files_folder.value
        master_file_name = master_file_path/RosDataset.master_filename.value
        if (not DataReader.is_file_valid(master_file_name)):
            print(f"Can't open Masterfile {master_file_name}")
            logger.critical(
                f"Can't open Masterfile {master_file_name}")
            raise FileNotFoundError
        self.topics = topics
        with master_file_name.open() as f: 
            self.__iterator_stotage = {}
            for line in f.read().splitlines():
                file = file_data_dir/line
                if (not DataReader.is_file_valid(file)):
                    logger.critical(
                        f"Can't open data file  {file.name}")
                    raise FileNotFoundError
                logger.info(f"open {file}")
                ros_file_storage = RosFileStorage(file)
                ros_file_storage.check_correct_topic(topics)
                self.__iterator_stotage[file] = ros_file_storage

            if(not any(self.__iterator_stotage)):
                logger.critical("empty Masterfile")
                raise Exception("empty Masterfile")
            logger.info("Creating Ros1IteratorDataset OK")
    
        self.iterator_files = self.__get_file_iterator()
        first_file = next(self.iterator_files)
        self.iterator_data = self.__iterator_stotage[first_file].get_iterator(topics = self.topics)
        
    def get_iterator(self, file: Path, topics: Iterable[str],  start: Optional[int] = None, stop: Optional[int] = None):
        ros_file_storage = self.__iterator_stotage[file]
        return ros_file_storage.get_iterator(topics = topics, start = start, stop = stop)
        
    def __next__(self):
        try:
            return next(self.iterator_data)
        except StopIteration:
            next_file = next(self.iterator_files) ### switch between files
            self.iterator_data = self.__iterator_stotage[next_file].get_iterator(topics = self.topics)
            logger.info(f"switch to new file {next_file}")
            return next(self.iterator_data)
        
    def __get_file_iterator(self):
        for file in self.__iterator_stotage.keys():
            yield file
    


class Ros1BagReader(DataReader):
    def __init__(self, config_path: Path = ConfigFilePaths.data_reader_config.value,
                       master_file_path: Optional[Path] = None,
                       raw_data: bool = False):
        super().__init__()
        self.__break_point = StoppingCriterionSingleton()
        self.raw_data = raw_data
        
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
                if(self.raw_data):
                    data = rawdata
                else:
                    data = deserialize_cdr(ros1_to_cdr(rawdata, msgtype), msgtype)
                break
            else:
                logger.info(f"topic {topic} is ignored")

        location = {"file": file,
                    "topic": topic}
        if(self.raw_data):
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

