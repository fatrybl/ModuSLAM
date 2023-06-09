import logging
from utils.config import Config
from configs.paths.DEFAULT_FILE_PATHS import ConfigFilePaths
from data_manager.batch_factory.data_batch import DataBatch


class FrontendManager:
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.measurements_processor = MeasurementsProcessor()
        self.graph_builder = GraphBuilder()
        self.config = Config(ConfigFilePaths.frontend_manager_config)
        if self.config.attributes.loop_detector:
            self.loop_detector = LoopDetector()
        if self.config.attributes.anomaly_detector:
            self.anomaly_detector = AnomalyDetector()

    def process(self, batch: DataBatch):
        self.measurements_processor.distribute_data(batch)
        self.measurements_processor.create_measurements()
        self.graph_builder.create_factors()
        self.graph_builder.add_factors_to_graph()
        batch.delete_used_data()
