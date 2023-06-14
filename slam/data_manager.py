import logging
from slam.data_manager.factory import BatchFactory
from slam.data_manager.data_filter import RawDataFilter
from slam.data_manager.factory.data_batch import DataBatch
from slam.utils.stopping_criterion import StoppingCriterion
from utils.config import Config
from configs.paths.DEFAULT_FILE_PATHS import ConfigFilePaths


class DataManager():
    logger = logging.getLogger(__name__)

    def __init__(self) -> None:
        self.batch_factory = BatchFactory()
        self.config = Config(ConfigFilePaths.data_manager_config)
        if self.config.attributes.use_filter:
            self.data_filter = RawDataFilter()

    def make_batch(self) -> DataBatch:
        self.batch_factory.create()
        if self.data_filter:
            self.data_filter.filter(self.batch_factory.batch)
