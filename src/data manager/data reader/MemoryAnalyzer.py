import psutil

class MemoryAnalyzer:
    def __init__(self):
        self.TotalRAM = self.get_total_ram()
        self.MaxBatchSize = None
        self.Percent = 0.8  # percent of available ram to be used for batch

    @staticmethod
    def get_total_ram():
        return psutil.virtual_memory().total

    @staticmethod
    def get_available_ram():
        return psutil.virtual_memory().available

    def calculate_max_batch_size(self, object_size):
        """
        Calculates max size of data batch in bytes
        """
        AvailableRam = self.get_available_ram()
        if object_size >= AvailableRam or (
                object_size >= self.Percent * AvailableRam and object_size <= AvailableRam):
            self.MaxBatchSize = self.Percent * AvailableRam
        else:
            self.MaxBatchSize = object_size

        return self.MaxBatchSize

    def is_enough_ram(self, object_size):
        AvailableRam = self.get_available_ram()
        if object_size >= AvailableRam:
            return False
        else:
            return True
