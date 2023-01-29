import psutil
from pathlib2 import Path
from rosbags.rosbag1 import Reader as RosBagReader
from rosbags.serde import deserialize_cdr, ros1_to_cdr
from math import ceil
from bagpy import bagreader
"""
DataReader reads data from file and send to Data Analyzer module.
params: size of data batch, file path
output: batch of raw data
"""

class FileReader:
    def __init__(self):
        self.BatchSize = None
        self.NumBatches = None
        self.AllowedFilesList = ['.bag', '.csv', '.json', '.txt']

    def is_correct_type(self, file_path):
        if file_path.suffix in self.AllowedFilesList:
            return True
        else:
            return False

    def check_file(self, file_path):
        """
        Checks data file before reading
        """
        if not Path.is_file(file_path):
            raise FileNotFoundError

        if not self.is_correct_type(file_path):
            raise TypeError('Incorrect type of input file. Allowed types are: ', self.AllowedFilesList)

        FileSize = file_path.stat().st_size # size in bytes
        if FileSize == 0:
            raise Exception("Empty input file")

    def choose_file_reader(self, file_path):
        FileType = file_path.suffix
        Reader = None
        if FileType == '.bag':
            Reader = RosBagReader
        elif FileType == '.csv':
            pass
        elif FileType == '.txt':
            pass
        elif FileType == '.json':
            pass
        else:
            raise NotImplementedError(f"A reader for the file type {FileType} has not been implemented")
        return Reader

    def read_file(self, file_path, Reader, batch_size=None):

        with Reader(file_path) as reader:
            # topic and msgtype information is available on .connections list
            print(reader.indexes[0])
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

if __name__ == "__main__":
    file_reader = FileReader()
    file_path = Path('/home/mark/Desktop/work/bags/Carla/carla-simulator-town2_n1-006_2022-10-27-14-28-04Z.evo1h_record_default.bag')
    file_reader.read_file(file_path, RosBagReader)


