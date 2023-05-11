class DataManager():
    def __init__(self):
        self.initializer = DataManagerInitializer()
        
        self.data_loader = DataLoader()
        self.memory_analyzer = MemoryAnalyzer()
        self.chunk_provider = ChunkProvider()
        self.raw_data_filter = DataFilter()
    
    def itinialize(self):
        pass

    def check_memory_usage(self):
        pass

    def filter_data(self):
        pass

    def make_data_chunk(self):
        pass