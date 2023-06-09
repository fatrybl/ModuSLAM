import csv
import logging
from pathlib2 import Path

from configs.paths.DEFAULT_FILE_PATHS import ConfigFilePaths
from utils.config import Config
from rosbags.rosbag1 import Reader as RosBagReader
from rosbags.serde import deserialize_cdr, ros1_to_cdr
import json

class FileReader():
    logger = logging.getLogger(__name__)

    def __init__(self, file_path: Path):
        self._file_name = file_path.stem
        self._file_type = file_path.suffix
        self._file_size = file_path.stat().st_size
        self._is_file_processed = False
        self._current_position = None
        self._config = Config(ConfigFilePaths.file_reader_config)
    
    @staticmethod
    def check_file(file_path: Path) -> bool:
        if not Path.is_file(file_path):
            raise FileNotFoundError

        if file_path.stat().st_size == 0:
            raise OSError("Empty input file")

    @staticmethod   
    def map_file2reader(file_path:Path):
        file_type = file_path.suffix
        if file_type == '.csv':
            return CsvReader()
        if file_type == '.bag':
            return Ros1BagReader()
        if file_type == '.mcap' or file_type == '.db3':
            return Ros2BagReader()
        
    @classmethod
    def create(cls, file_path:Path):
        return cls.map_file2reader(file_path)
            


class CsvReader(FileReader):
    def __init__(self, file_path:Path):
        super().__init__(file_path) 
        self.__newline = self._config.attributes.csv_file.newline
        self.__delimiter = self._config.attributes.csv_file.delimiter
        self.__quotechar = self._config.attributes.csv_file.quotechar

    def get_element(self, file_path: Path):
        self.check_file(file_path)
        with open(file_path,'r', newline=self.__newline) as f:
            reader = csv.reader(f, delimiter=self.__delimiter, quotechar=self.__quotechar)
            row = next(reader)
            self._current_position = reader.line_num
        return row
    

class Ros1BagReader(FileReader):
    def __init__():
        super().__init__()

    def get_element(self, file_path: Path):
        pass


class Ros2BagReader(FileReader):
    def __init__():
        super().__init__()

    def get_element(self, file_path: Path):
        pass











    
    def read(self, file_path, topics, batch_size=None):
        self.__check_file()
        size = 0
        current_message_idx = 0
        with RosBagReader(file_path) as reader:
            connections = [x for x in reader.connections if x.topic in topics]
            print('bag duration: ', (reader.end_time-reader.start_time)*1e-9, 'sec.')
            print('messages num:', reader.message_count)
            print('indexes num:', len(reader.indexes))
            print('connections num:', len(reader.connections))
            print('chunks num: ', len(reader.chunks))
            print('topics num: ', len(reader.topics))
            print(reader.current_chunk)
            prev_t = reader.start_time
            with open('data_config.json') as json_file:
                data = json.load(json_file)
            for i, message in enumerate(reader.messages(connections=connections)):
                connection, timestamp, rawdata = message
                data["time"].append(timestamp)
                data["id"].append(i)
                if prev_t == timestamp
            print(pd.DataFrame.from_dict(data, orient='columns').set_index("id"))
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


