import logging
from pathlib import Path
from typing import  Optional, Iterable

from rosbags.rosbag1 import Reader

from configs.paths.DEFAULT_FILE_PATHS import RosDataset
from slam.data_manager.factory.readers.data_reader import DataReader


logger = logging.getLogger(__name__)

class RosFileStorage():
    def __init__(self, file: Path):
        self.file = file

    def check_topics(self, topics: Iterable[str]):
        with Reader(self.file) as reader: 
            if(reader.message_count == 0):
                logger.critical(f"Empty Rosbag file {self.file.name}")
            logger.debug(f"file {self.file.name} has available topics {reader.topics.keys()}")
            
            for topic_name in topics:
                if topic_name not in reader.topics.keys():
                    logger.critical(f"there are no topic {topic_name} ")
                    raise KeyError
            
    def get_iterator(self, topics: Iterable[str],  start: Optional[int] = None, stop: Optional[int] = None):
        with Reader(self.file) as reader: 
            connections = []
            for topic in topics:
                connections.append(*reader.topics[topic].connections)
            for line in reader.messages(connections = connections, start = start, stop = stop):
                connection, timestamp, rawdata = line
                yield self.file, connection.topic, connection.msgtype, timestamp, rawdata

        
class RosDatasetIterator():
    def __init__(self, master_file_dir:Path, topics: Iterable[str]):
        file_data_dir = master_file_dir/RosDataset.data_files_folder.value
        master_file_name = master_file_dir/RosDataset.master_filename.value
        if (not DataReader._is_file_valid(master_file_name)):
            print(f"Can't open Masterfile {master_file_name}")
            logger.critical(
                f"Can't open Masterfile {master_file_name}")
            raise FileNotFoundError
        self.topics = topics
        with master_file_name.open() as f: 
            self.__file_stotage = {}
            for line in f.read().splitlines():
                file = file_data_dir/line
                if (not DataReader._is_file_valid(file)):
                    logger.critical(
                        f"Can't open data file {file.name}")
                    raise FileNotFoundError
                logger.debug(f"open {file}")
                ros_file_storage = RosFileStorage(file)
                ros_file_storage.check_topics(topics)
                self.__file_stotage[file] = ros_file_storage

            if(not any(self.__file_stotage)):
                logger.critical("empty Masterfile")
                raise Exception("empty Masterfile")
            logger.debug("Creating Ros1IteratorDataset OK")
    
        self.__file_iterator = self.__get_file_iterator()
        first_file = next(self.__file_iterator)
        self.__data_iterator = self.__file_stotage[first_file].get_iterator(topics = self.topics)
        
    def get_iterator(self, file: Path, topics: Iterable[str],  start: Optional[int] = None, stop: Optional[int] = None):
        ros_file_storage = self.__file_stotage[file]
        return ros_file_storage.get_iterator(topics = topics, start = start, stop = stop)
        
    def __next__(self):
        try:
            return next(self.__data_iterator)
        except StopIteration:
            next_file = next(self.__file_iterator) ### switch between files
            self.__data_iterator = self.__file_stotage[next_file].get_iterator(topics = self.topics)
            logger.debug(f"switch to new file {next_file}")
            return next(self.__data_iterator)
        
    def __get_file_iterator(self):
        for file in self.__file_stotage.keys():
            yield file
    