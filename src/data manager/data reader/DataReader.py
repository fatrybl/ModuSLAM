import psutil
from pathlib2 import Path
from rosbags.rosbag1 import Reader as RosBagReader
from math import ceil

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
        else:
            raise NotImplementedError(f"A reader for the file type {FileType} has not been implemented")
        return Reader

    def read_file(self, data_file_path, batch_size, reader):
        return reader.read(data_file_path, batch_size)


