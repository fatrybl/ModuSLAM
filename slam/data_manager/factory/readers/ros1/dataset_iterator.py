import logging
from pathlib import Path
from typing import  Optional, Iterator
from dataclasses import dataclass

from rosbags.rosbag1 import Reader

from slam.utils.exceptions import  TopicNotFound
from slam.data_manager.factory.readers.element_factory import Location


@dataclass(frozen=True)
class RosElementLocation(Location):
    file: Path
    topic: str
    msgtype: str

@dataclass
class RosDataRange():
    topics: list[str] = None
    start: Optional[int] = None
    stop: Optional[int] = None

logger = logging.getLogger(__name__)

class RosFileStorage():
    def __init__(self, file: Path):
        self.file: Path = file
        self.start_time = None
        self.end_time = None

    def check_topics(self, topics: list[str]):
        with Reader(self.file) as reader: 
            self.start_time = reader.start_time
            self.end_time = reader.end_time
            if(reader.message_count == 0):
                msg = f"Empty Rosbag file {self.file.name}"
                logger.critical(msg)
            msg = f"file {self.file.name} has available topics {reader.topics.keys()}"
            logger.debug(msg)
            for topic_name in topics:
                if topic_name not in reader.topics.keys():
                    msg = f"there are no topic {topic_name} "
                    logger.critical(msg)
                    raise TopicNotFound
            
    def get_data_iterator(self, location: RosDataRange) -> Iterator[tuple[RosElementLocation, int,  bytes]]:
        with Reader(self.file) as reader: 
            connections = []
            for topic in location.topics:
                connections.append(*reader.topics[topic].connections)

            for line in reader.messages(connections = connections, start = location.start, stop = location.stop):
                connection, timestamp, rawdata = line
                loc = RosElementLocation(self.file, connection.topic, connection.msgtype)
                yield loc, timestamp, rawdata

class RosDatasetIterator():
    def __init__(self, file_storages: list[RosFileStorage], location: RosDataRange):
        self.__file_storages: list[RosFileStorage] = file_storages
        if(len(file_storages) == 0):
            msg = "empty list of file_storages"
            logger.critical(msg)
            raise ValueError(msg)
        
        self.__location: RosDataRange = location
        self.__file_iterator : Iterator[RosFileStorage] = self.__get_file_iterator()
        first_file_storege: RosFileStorage = next(self.__file_iterator) 
        self.__data_iterator: Iterator[tuple[RosElementLocation, int, bytes]]  = first_file_storege.get_data_iterator(self.__location)
        
    def __next__(self) -> tuple[RosElementLocation, int, bytes]:
        try:
            loc, timestamp, rawdata = next(self.__data_iterator)
            return loc, timestamp, rawdata
        except StopIteration:
            next_file_store: RosFileStorage = next(self.__file_iterator) ### switch between files
            self.__data_iterator = next_file_store.get_data_iterator(self.__location)
            logger.debug(f"switch to new file {next_file_store.file}")
            return next(self.__data_iterator)
        
    def __get_file_iterator(self) -> Iterator[RosFileStorage]:
        for file_store in self.__file_storages:
            yield file_store

