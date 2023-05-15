"""
class for filtering dummy measurements which could never happen
"""
class RawDataFilter():
    def __init__(self):
        self.a = 0
        self.setup()
    
    def setup(self):
        cfg = Config()
        cfg.load_config()
        
    def filter_empty_messages(self):
        pass
    def filter_extreme_values(self):
        pass

