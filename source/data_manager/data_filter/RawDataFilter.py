"""
Filter of dummy unrealistic measurements
"""
import logging

class RawDataFilter():
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.a = 0
        self.setup()
    
    def setup(self):
        cfg = Config()
        
    def filter_empty_messages(self):
        pass
    def filter_extreme_values(self):
        pass

