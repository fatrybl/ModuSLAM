from pathlib2 import Path


class BatchFactoryParameters():
    def __init__(self):
        self.data_directory_path = Path()
        self.filenames_list = []
        self.ram_usage_percentage = float()
        self.batch_size = float()
