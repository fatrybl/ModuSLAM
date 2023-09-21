import logging
from plum import dispatch
from pathlib import Path
from typing import  Optional
from typing import Type
from rosbags.serde import deserialize_cdr, ros1_to_cdr
from dataclasses import dataclass, field

from configs.paths.DEFAULT_FILE_PATHS import ConfigFilePaths
from slam.data_manager.factory.readers.data_reader import DataReader
from slam.data_manager.factory.readers.element_factory import Element, Measurement
from slam.utils.config import Config
from slam.data_manager.factory.readers.ros1.dataset_iterator import RosDatasetIterator, RosFileRangeLocation
from slam.utils.exceptions import NotSubset
from slam.setup_manager.sensor_factory.sensor_factory import SensorFactory
from slam.setup_manager.sensor_factory.sensors import Sensor

# @dataclass
# class RosConfig():
#     topics: Iterable[str]
#     start: Optional[int] = None
#     stop: Optional[int] = None

logger = logging.getLogger(__name__)

# class SensorFactoryModifyd(SensorFactory):
#         self.sensors: set[Type[Sensor]] = set()
#         cfg = Config.from_file(paths.data_manager_config.value)
#         self.attributes: dict[str, str] = cfg.attributes['sensors']
#         self._init_sesnors()
#         self._check_used_sesnors()
class Ros1BagReader(DataReader):
    def __init__(self, data_reader_conf_path: Path = ConfigFilePaths.data_reader_config.value,
                       deserialize_raw_data: bool = False,
                       master_file_dir: Optional[Path] = None):
        super().__init__()
        self.deserialize_raw_data = deserialize_raw_data

        if(master_file_dir == None):
            config = Config.from_file(ConfigFilePaths.data_manager_config.value)
            master_file_dir = Path(config.attributes["data"]["dataset_directory"])

        cfg: Config = Config.from_file(data_reader_conf_path)

        used_sensors: set[str] = set(cfg.attributes["used_sensors"])
        topic_sensor_cfg = cfg.attributes["ros1_reader"]["used_topics"]
        self.__topic_sensor_dict = dict()
        for sensor in used_sensors:
            if(sensor not in topic_sensor_cfg):
                logger.critical(f"no topic for  {sensor} in config, available sensors are {topic_sensor_cfg}")
                raise NotSubset
            topic: str = topic_sensor_cfg[sensor]
            self.__topic_sensor_dict[topic] = sensor

        logger.debug(f"available topics in RosReader: {self.__topic_sensor_dict.keys()}")
        self.__sensor_factory = SensorFactory()
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
                sensor_name: str = self.__topic_sensor_dict[topic]
                #sensor: Type[Sensor] = self.__sensor_factory.name_to_sensor(sensor_name)
                if(self.deserialize_raw_data):
                    msgtype = location.msgtype
                    data = deserialize_cdr(ros1_to_cdr(rawdata, msgtype), msgtype)
                else:
                    data = rawdata
                break

        sensor = sensor_name
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

