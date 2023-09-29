import logging
from pathlib import Path
from typing import  Optional, Iterable, Iterator
from dataclasses import dataclass

from rosbags.rosbag1 import Reader

from configs.paths.DEFAULT_FILE_PATHS import RosDatasetStructure
from slam.data_manager.factory.readers.data_reader import DataReader
from slam.utils.exceptions import FileNotValid, TopicNotFound
from slam.data_manager.factory.readers.element_factory import Location
from slam.utils.exceptions import Wrong_data

@dataclass
class RosElementLocation(Location):
    file: Path
    topic: str
    msgtype: str

@dataclass
class RosDataRange():
    topics: Iterable[str] = None
    start: Optional[int] = None
    stop: Optional[int] = None

logger = logging.getLogger(__name__)

class RosFileStorage():
    def __init__(self, file: Path):
        self.file: Path = file
        self.start_time = None
        self.end_time = None

    def check_topics(self, topics: Iterable[str]):
        with Reader(self.file) as reader: 
            self.start_time = reader.start_time
            self.end_time = reader.end_time
            if(reader.message_count == 0):
                logger.critical(f"Empty Rosbag file {self.file.name}")
            logger.debug(f"file {self.file.name} has available topics {reader.topics.keys()}")
            
            for topic_name in topics:
                if topic_name not in reader.topics.keys():
                    logger.critical(f"there are no topic {topic_name} ")
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
        self.__location: RosDataRange = location
        self.__data_iterator: Iterator[tuple[RosElementLocation, int, bytes]]  = self.__file_storages[0].get_data_iterator(self.__location)
        self.__file_iterator : Iterator[RosFileStorage] = self.__get_file_iterator()
        self.__file_iterator.__next__()

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


        
class RosManager():
    def __init__(self, master_file_dir:Path, topics: Iterable[str]):
        file_data_dir: Path  = master_file_dir/RosDatasetStructure.data_files_folder.value
        master_file_name: Path = master_file_dir/RosDatasetStructure.master_filename.value
        if (not DataReader._is_file_valid(master_file_name)):
            logger.critical(
                f"Can't open Masterfile {master_file_name}")
            raise FileNotValid
        self.__topics: Iterable[str] = list(topics)
        self.__file_storage : dict[Path, RosFileStorage] = dict()
        self.__file_list: list[Path] = list()
        with master_file_name.open() as f: 
            for line in f.read().splitlines():
                file = file_data_dir/line
                if (not DataReader._is_file_valid(file)):
                    logger.critical(f"Can't open data file {file.name}")
                    raise FileNotValid
                logger.debug(f"open {file}")
                ros_file_storage: RosFileStorage = RosFileStorage(file)
                ros_file_storage.check_topics(topics)
                self.__file_storage[file] = ros_file_storage
                if(len(self.__file_list) > 0):
                    file_name_prev = self.__file_list[-1]
                    ros_file_storage_prev: RosFileStorage = self.__file_storage[file_name_prev]
                    if(ros_file_storage.start_time < ros_file_storage_prev.end_time):
                        logger.critical(f"wrong timestamp")
                        raise Wrong_data
                self.__file_list.append(file)
            logger.debug("Creating Ros1IteratorDataset OK")

    def get_main_iterator(self) -> RosDatasetIterator:
        """return iterator for main dataset

        Returns:
            RosDatasetIterator
        """
        return RosDatasetIterator([self.__file_storage[file] for file in self.__file_list], RosDataRange(topics=self.__topics))
    
    

    def get_iterator_from_file(self, file: Path,  location: RosDataRange) ->  RosDatasetIterator:
        """return iterator for dataset for given file and location
        Args:
            file (Path): 
            location (RosDataRange): 

        Returns:
            RosDatasetIterator: 
        """
        ros_file_storage: RosFileStorage = self.__file_storage[file]
        if(location.topics == None):
            location.topics = self.__topics
        return RosDatasetIterator([ros_file_storage], location)

    def get_iterator(self, location: RosDataRange) ->  RosDatasetIterator:
        """return iterator for dataset for given location
        Args:
            file (Path): 
            location (RosDataRange): 

        Returns:
            RosDatasetIterator: 
        """
        used_file_storages = []
        for file in self.__file_list:
            ros_file_storage: RosFileStorage = self.__file_storage[file]
            line_intersection1: bool  = (ros_file_storage.start_time  >= location.start and ros_file_storage.start_time <= location.stop) or \
                                        (ros_file_storage.end_time  >= location.start and ros_file_storage.end_time <= location.stop) 
            
            line_intersection2: bool  = (location.start  >= ros_file_storage.start_time and location.start <= ros_file_storage.end_time) or \
                                       (location.stop  >= ros_file_storage.start_time and location.stop <= ros_file_storage.end_time) 
            if(line_intersection1 or line_intersection2):
                used_file_storages.append(ros_file_storage)
        if(location.topics == None):
            location.topics = self.__topics

        return RosDatasetIterator(used_file_storages, location)
