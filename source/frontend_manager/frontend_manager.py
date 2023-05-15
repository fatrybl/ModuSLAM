class FrontendManager:
    def __init__(self):
        """
        base attributes
        """
        self.measurements_processor = MeasurementsProcessor()
        self.graph_builder = GraphBuilder()
    
    def setup(self):
        cfg = Config()

        if cfg.attributes.use_loop_closure:
            self.loop_detector = LoopDetector()
        if cfg.attributes.use_anomaly_detector:
            self.anomaly_detector = AnomalyDetector()

        
    def process_data_chunk(self, data):
        pass