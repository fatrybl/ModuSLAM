from rosbags.rosbag1 import Reader
from rosbags.serde import deserialize_cdr, ros1_to_cdr
from rosbags.interfaces import Connection
from pathlib import Path
from data_manager.factory.readers.data_reader import DataReader
import logging
from data_manager.factory.readers.element_factory import Element, Measurement
from slam.utils.stopping_criterion import StoppingCriterionSingleton
from configs.paths.DEFAULT_FILE_PATHS import RosDataset
from configs.paths.DEFAULT_FILE_PATHS import ConfigFilePaths
from slam.utils.config import Config
import numpy as np
#from slam.logger import logging_config
from typing import Iterable, Callable, Optional

logger = logging.getLogger(__name__)

class Ros1BagReader(DataReader):
    def __init__(self, config_path: Path = ConfigFilePaths.data_reader_config.value,
                       file_name_path: Path = None,
                       raw_data: bool = False):
        super().__init__()
        self.raw_data = raw_data
        if(file_name_path == None):
            self.file = self._dataset_dir / RosDataset.data_stamp.value
        else:
            self.file = file_name_path
        logger.info("Initializing Ros1BagReader: %s\n",self.file.name)
        cfg = Config.from_file(config_path)
        topic_info = cfg.attributes["ros1_reader"]["used_sensors"]
        self.__sensor_info = {k: v for d in topic_info for k, v in d.items()} #keqy - ros topic, value - sensor name
        logger.info("readable topics: %s\n",  self.__sensor_info.keys())
        self.__iterator = self.__init_iterator()
        self.__break_point = StoppingCriterionSingleton()

    def __init_iterator(self, topic: str = None,  start: Optional[int] = None, stop: Optional[int] = None):
        if (DataReader.is_file_valid(self.file)):
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
            
        else:
            logger.critical(
                f"Couldn't initialize the iterator for {self.file}")
            self.__break_point.is_data_processed = True
            raise ValueError
        
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
        return sensor, data, timestamp, location

    def get_element(self, iterator = None) -> Element:
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
            # print(measurement, location, timestamp)
            # print("----------------------------------------------------------")
            # if(location["position"] > 300000):
            #     raise StopIteration
            return Element(timestamp, measurement, location)

        except StopIteration:
            self.__break_point.is_data_processed = True
            logger.info("data finished")
            return None

        # except Exception as e:
        #     logger.exception(e)
        #     print("error", e)
        #     self.__break_point.is_data_processed = True
        #     raise e
    
    def get_element_with_measurement(self, measurement: tuple)-> Element:
        """
        Args:
            measurement: 
                {"sensor": "camera_rgb_left",
                "location": {"file": Path(),
                             "position": 0}  }
        Gets element from dataset with particular sensor measurement.
        Should be implemented for each reader
        """
        location = measurement["location"]
        timestamp = measurement["timestamp"]
        topic = location["topic"]

        iterator = self.__init_iterator(topic = topic, start = timestamp, stop = timestamp+1)
        element = self.get_element(iterator)
        return element

    
# def read(self, file_path, topics, batch_size=None):
    #     self.__check_file()
    #     size = 0
    #     current_message_idx = 0
    #     with RosBagReader(file_path) as reader:
    #         connections = [x for x in reader.connections if x.topic in topics]
    #         print('bag duration: ', (reader.end_time-reader.start_time)*1e-9, 'sec.')
    #         print('messages num:', reader.message_count)
    #         print('indexes num:', len(reader.indexes))
    #         print('connections num:', len(reader.connections))
    #         print('chunks num: ', len(reader.chunks))
    #         print('topics num: ', len(reader.topics))
    #         print(reader.current_chunk)
    #         prev_t = reader.start_time
    #         with open('data_config.json') as json_file:
    #             data = json.load(json_file)
    #         for i, message in enumerate(reader.messages(connections=connections)):
    #             connection, timestamp, rawdata = message
    #             data["time"].append(timestamp)
    #             data["id"].append(i)
    #             if prev_t == timestamp
    #         print(pd.DataFrame.from_dict(data, orient='columns').set_index("id"))
        #     if(t == prev_t):
        #         print('True')
        #     prev_t = t
        # for con in connections:
        # for message in reader.messages(connections=[con]):
        #         connection, timestamp, rawdata = message
        #         msg = deserialize_cdr(ros1_to_cdr(rawdata, connection.msgtype), connection.msgtype)
        #         print(reader.read_chunk())
        # print(msg.header.frame_id)

        # dataFrames = [pd.DataFrame()]*len(generators)
        #     for gen in generators:
        #         for connection, timestamp, rawdata in gen:
        #             msg = deserialize_cdr(ros1_to_cdr(rawdata, connection.msgtype), connection.msgtype)
        #             print(msg.header.frame_id)
        #         # for message in gen:
        #         #     connection, timestamp, rawdata = message
        #         #     msg = deserialize_cdr(ros1_to_cdr(rawdata, connections.msgtype), connections.msgtype)
        #
        #     # connection, timestamp, rawdata = next(gen)
        #     # msg = deserialize_cdr(ros1_to_cdr(rawdata, connection.msgtype), connection.msgtype)
        #     # tmp.append(msg)
        #     start_mem = psutil.Process().memory_info().rss / (1024**2)
        #     # print(type(msg.orientation))
        #     for i, message in enumerate(gen):
        #         connection, timestamp, rawdata = message
        #         msg = deserialize_cdr(ros1_to_cdr(rawdata, connection.msgtype), connection.msgtype)
        #         tmp.append(msg)
        #         current_RAM_used = psutil.Process().memory_info().rss / (1024 ** 2) - start_mem
        #         # print(current_RAM_used)
        #         if current_RAM_used >= batch_size:
        #             print('!!!!!!', current_RAM_used)
        #             break
        # print('sum= ',start_mem + current_RAM_used)
        # print('total= ',psutil.Process().memory_info().rss / (1024 ** 2))
        #     print(i)
        # while current_message_idx <  reader.message_count or size < batch_size:

        # topic and msgtype information is available on .connections list
        # imu_connections = [x for x in reader.connections if x.topic == '/sensors/imu_driver/imu']
        # gen = reader.messages(connections=imu_connections)
        # for message in gen:
        #     connection, timestamp, rawdata = message
        #     msg = deserialize_cdr(ros1_to_cdr(rawdata, connection.msgtype), connection.msgtype)
        #     print(msg.angular_velocity.x)
        # msg = deserialize_cdr(ros1_to_cdr(rawdata, connection.msgtype), connection.msgtype)
        # print(msg.angular_velocity.x)
        # print(msg.header.frame_id)
        #
        # for connection in reader.connections:
        #     print(connection.topic, connection.msgtype)
        #
        # # iterate over messages
        # for connection, timestamp, rawdata in reader.messages():
        #     if connection.topic == '/sensors/imu_driver/imu':
        #         msg = deserialize_cdr(ros1_to_cdr(rawdata, connection.msgtype), connection.msgtype)
        #         print(msg.header.frame_id)
        #
        # # messages() accepts connection filters
        # connections = [x for x in reader.connections if x.topic == '/sensors/imu_driver/imu']
        # for connection, timestamp, rawdata in reader.messages(connections=connections):
        #     msg = deserialize_cdr(ros1_to_cdr(rawdata, connection.msgtype), connection.msgtype)
        #     print(msg.header.frame_id)
