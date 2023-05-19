import logging

class FrontendManager:
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.measurements_processor = MeasurementsProcessor()
        self.graph_builder = GraphBuilder()
    
    def setup(self):
        cfg = Config()

        if cfg.attributes.loop_detector:
            self.loop_detector = LoopDetector()

        if cfg.attributes.anomaly_detector:
            self.anomaly_detector = AnomalyDetector()

        
    def process_data_chunk(self, data):
        pass