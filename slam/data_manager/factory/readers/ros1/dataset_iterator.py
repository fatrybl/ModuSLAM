import logging
from pathlib import Path
from typing import  Optional, Iterable, Iterator
from dataclasses import dataclass, field

from rosbags.rosbag1 import Reader

from configs.paths.DEFAULT_FILE_PATHS import RosDatasetStructure
from slam.data_manager.factory.readers.data_reader import DataReader
from slam.utils.exceptions import FileNotValid, TopicNotFound
from slam.data_manager.factory.readers.element_factory import Location


@dataclass
class RosElementLocation(Location):
    file: Path
    topic: str
    msgtype: str
    timestamp: int

@dataclass
class RosFileRangeLocation():
    topics: Iterable[str]
    start: Optional[int] = None
    stop: Optional[int] = None

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
                    raise TopicNotFound
            
    def get_iterator(self, location: RosFileRangeLocation) -> Iterator[tuple[RosElementLocation, bytes]]:
        with Reader(self.file) as reader: 
            connections = []
            for topic in location.topics:
                connections.append(*reader.topics[topic].connections)
            for line in reader.messages(connections = connections, start = location.start, stop = location.stop):
                connection, timestamp, rawdata = line
                loc = RosElementLocation(self.file, connection.topic, connection.msgtype, timestamp)
                yield loc, rawdata

        
class RosDatasetIterator():
    def __init__(self, master_file_dir:Path, topics: Iterable[str]):
        file_data_dir: Path  = master_file_dir/RosDatasetStructure.data_files_folder.value
        master_file_name: Path = master_file_dir/RosDatasetStructure.master_filename.value
        if (not DataReader._is_file_valid(master_file_name)):
            print(f"Can't open Masterfile {master_file_name}")
            logger.critical(
                f"Can't open Masterfile {master_file_name}")
            raise FileNotValid
        self.topics: Iterable[str] = topics
        self.__file_stotage = dict()
        with master_file_name.open() as f: 
            for line in f.read().splitlines():
                file = file_data_dir/line
                if (not DataReader._is_file_valid(file)):
                    logger.critical(
                        f"Can't open data file {file.name}")
                    raise FileNotValid
                logger.debug(f"open {file}")
                ros_file_storage = RosFileStorage(file)
                ros_file_storage.check_topics(topics)
                self.__file_stotage[file] = ros_file_storage
            logger.debug("Creating Ros1IteratorDataset OK")
    
        self.__file_iterator: Iterator[Path] = self.__get_file_iterator()
        first_file: Path = next(self.__file_iterator)
        self.__data_iterator: Iterator[tuple[RosElementLocation, bytes]]  = self.__file_stotage[first_file].get_iterator(RosFileRangeLocation(topics = self.topics))

    def __next__(self):
        try:
            return next(self.__data_iterator)
        except StopIteration:
            next_file = next(self.__file_iterator) ### switch between files
            self.__data_iterator = self.__file_stotage[next_file].get_iterator(RosFileRangeLocation(topics = self.topics))
            logger.debug(f"switch to new file {next_file}")
            return next(self.__data_iterator)    
        
    def get_iterator(self, file: Path,  location: RosFileRangeLocation) ->  Iterator[tuple[RosElementLocation, bytes]]:
        ros_file_storage = self.__file_stotage[file]
        return ros_file_storage.get_iterator(location)
    
    def __get_file_iterator(self) -> Iterator[Path]:
        for file in self.__file_stotage.keys():
            yield file
    