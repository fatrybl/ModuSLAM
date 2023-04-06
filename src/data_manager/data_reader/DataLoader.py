from MemoryAnalyzer import MemoryAnalyzer
from DataReader import FileReader
from src.data_manager.data_synchronizer.MeasurementsSynchronizer import MeasurementsSynchronizer as Synchronizer
class DataLoader:
    def __init__(self, data_file_path, batch_size=None, mode='full batch'):
        self.Mode = mode
        self.DataFilePath = data_file_path
        self.BatchSize = self.calculate_batch_size(batch_size)
        self.CurrentFreeRam = MemoryAnalyzer.get_available_ram()
        self.NumBatches = None
        self.Status = None
        self.Data = None
        self.isDataAvailable = False
        self.Synchronizer = MeasurementsSynchronizer()
        self.Reader = FileReader()

    def update_status(self):
        if self.Reader.isUnprocessedDataLeft:
            self.isDataAvailable = True
        else:
            self.isDataAvailable = False

    def calculate_batch_size(self, batch_size):
        if batch_size is None:
            """
            some code here to compute batch size
            """
            pass
        else:
            return batch_size

    def read_data(self):
        self.Data = self.Reader.read_file(self.DataFilePath, self.BatchSize)

    def convert_to_csv(self):
        pass
