class FrontendManagerParameters(ObjectParameters):
    def __init__(self) -> None:
        super().__init__()
        self.graph_builder = GraphBuilderParameters()
        self.loop_closure = LoopClosureParameters()
        self.anomaly_detector = AnomalyDetectorParameters()
        