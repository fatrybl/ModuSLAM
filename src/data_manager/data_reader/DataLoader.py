from MemoryAnalyzer import MemoryAnalyzer
from DataReader import FileReader
class DataLoader:
    def __init__(self, data_file_path, batch_size=None, mode='full batch'):
        self.Mode = mode
        self.DataFilePath = data_file_path
        self.BatchSize = self.calculate_batch_size(batch_size)
        self.CurrentFreeRam = MemoryAnalyzer.get_available_ram()
        self.NumBatches = None
        self.Status = None
        self.Data = None

    def calculate_batch_size(self, batch_size):
        if batch_size is None:
            """
            some code here to compute batch size
            """
            pass
        else:
            return batch_size

    def read_data(self):
        Reader = FileReader()
        return Reader.read_file(self.DataFilePath, self.BatchSize)

    def split_data(self):
        BatchList = []
        num_batches = ceil(file_size / BatchSize)
        return BatchList
