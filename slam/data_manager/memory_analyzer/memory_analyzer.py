import psutil

class MemoryAnalyzer():
    DEFAULT_MEMORY_PERCENT = 0.5

    def __init__(self):
        self.total_memory = psutil.virtual_memory().total
        self.available_memory = psutil.virtual_memory().available
        self.used_memory_percent = psutil.virtual_memory().percent
        self.allowed_memory_percent = MemoryAnalyzer.DEFAULT_MEMORY_PERCENT
        self.setup()
    
    def setup(self):
        cfg = Config()
        self.allowed_memory_percent = cfg.attributes.batch_memory_percent
