class DataManager():
    def __init__(self):
        """
        base attributes
        """
        self.data_loader = DataLoader()
        self.memory_analyzer = MemoryAnalyzer()
        self.chunk_provider = ChunkProvider()
    
    def setup(self):
        cfg = Config()
        
        if cfg.use_filter:
            self.raw_data_filter = DataFilter()
        if cfg.use_something:
            self.something = Something()

    def check_memory_usage(self):
        pass

    def filter_data(self):
        pass

    def make_data_chunk(self):
        pass