class FrontendManager:
    def __init__(self):
        self.initializer = FrontendManagerInitializer()
        self.measurements_processor = MeasurementsProcessor()
        self.graph_builder = GraphBuilder()
        self.anomaly_detector = AnomalyDetector()
        self.loop_detector = LoopDetector()
        
    def process_data_chunk(self, data):
        pass