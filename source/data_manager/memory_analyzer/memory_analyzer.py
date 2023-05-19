import psutil

class MemoryAnalyzer():
    def __init__(self):
        self.a = 0
        self.setup()
    
    def setup(self):
        cfg = Config()
        cfg.load_config()
        
        if cfg.use_full_ram:
            pass
        if cfg.use_something:
            self.something = Something()

