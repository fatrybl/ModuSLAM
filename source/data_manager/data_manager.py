import logging

class DataManager():
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.batch_factory = BatchFactory()
        self.chunk_factory = ChunkFactory()
        self.memory_analyzer = MemoryAnalyzer()
    
    def setup(self):
        cfg = Config()
        
        if cfg.use_filter:
            self.data_filter = DataFilter()

    def check_memory_usage(self):
        pass

    def filter_data(self):
        pass

    def make_data_chunk(self):
        pass