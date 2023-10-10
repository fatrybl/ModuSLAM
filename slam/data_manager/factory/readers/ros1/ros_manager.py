
from pathlib import Path
import logging
from plum import dispatch

from configs.experiments.ros1.config import RosDatasetStructure
from slam.data_manager.factory.readers.data_reader import DataReader
from slam.data_manager.factory.readers.ros1.dataset_iterator import RosFileStorage, RosDatasetIterator, RosDataRange
from slam.utils.exceptions import FileNotValid
logger = logging.getLogger(__name__)

class RosManager():
    def __init__(self, master_file_dir:Path, topics: list[str]):
        file_data_dir: Path  = master_file_dir/RosDatasetStructure.data_files_folder.value
        master_file_name: Path = master_file_dir/RosDatasetStructure.master_filename.value
        if (not DataReader._is_file_valid(master_file_name)):
            msg = f"Can't open Masterfile {master_file_name}"
            logger.critical(msg)
            raise FileNotValid
        self.__topics: list[str] = topics
        self.__file_storage : dict[Path, RosFileStorage] = dict()
        self.__file_list: list[Path] = list()
        with master_file_name.open() as f: 
            for line in f.read().splitlines():
                file: Path = file_data_dir/line
                if (not DataReader._is_file_valid(file)):
                    msg = f"Can't open data file {file.name}"
                    logger.critical(msg)
                    raise FileNotValid
                msg = f"open {file}"
                logger.debug(msg)
                ros_file_storage: RosFileStorage = RosFileStorage(file)
                ros_file_storage.check_topics(topics)
                self.__check_valid_timestamp(ros_file_storage)
                self.__file_storage[file] = ros_file_storage  
                self.__file_list.append(file)
            msg = "Creating Ros1IteratorDataset OK"
            logger.debug(msg)

    def __check_valid_timestamp(self, ros_file_storage: RosFileStorage):
        if(len(self.__file_list) > 0):
            file_name_prev: Path = self.__file_list[-1]
            ros_file_storage_prev: RosFileStorage = self.__file_storage[file_name_prev]
            if(ros_file_storage.start_time < ros_file_storage_prev.end_time):
                msg = f"wrong timestamp in file {file_name_prev.value}"
                logger.critical(msg)
                raise ValueError(msg)
            
    @dispatch       
    def get_iterator(self) -> RosDatasetIterator:
        """return iterator for main dataset
        Returns:
            RosDatasetIterator
        """
        filestorages: list[RosFileStorage] = [self.__file_storage[file] for file in self.__file_list]
        data_range = RosDataRange(topics = self.__topics)
        return RosDatasetIterator(filestorages, data_range)
    
    

    @dispatch
    def get_iterator(self, file: Path,  data_range: RosDataRange) ->  RosDatasetIterator:
        """return iterator for dataset for given file and data_range
        Args:
            file (Path): 
            data_range (RosDataRange): 

        Returns:
            RosDatasetIterator: 
        """
        ros_file_storage: RosFileStorage = self.__file_storage[file]
        if not data_range.topics:
            data_range.topics = self.__topics
        return RosDatasetIterator([ros_file_storage], data_range)
    


    @dispatch
    def get_iterator(self, data_range: RosDataRange) ->  RosDatasetIterator:
        """return iterator for dataset for given data_range
        Args:
            file (Path): 
            data_range (RosDataRange): 

        Returns:
            RosDatasetIterator: 
        """
        used_file_storages: list[RosFileStorage] = []
        for file in self.__file_list:
            ros_file_storage: RosFileStorage = self.__file_storage[file]
            intersection1: bool  = (ros_file_storage.start_time  >= data_range.start and ros_file_storage.start_time <= data_range.stop) or \
                                        (ros_file_storage.end_time  >= data_range.start and ros_file_storage.end_time <= data_range.stop) 
            
            intersection2: bool  = (data_range.start  >= ros_file_storage.start_time and data_range.start <= ros_file_storage.end_time) or \
                                       (data_range.stop  >= ros_file_storage.start_time and data_range.stop <= ros_file_storage.end_time) 
            if(intersection1 or intersection2):
                used_file_storages.append(ros_file_storage)
        if not data_range.topics:
            data_range.topics = self.__topics

        return RosDatasetIterator(used_file_storages, data_range)
