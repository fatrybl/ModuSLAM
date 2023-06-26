import logging
from data_manager.factory.batch_factory import BatchFactory
from data_manager.filter.data_filter import RawDataFilter
from utils.config import Config
from configs.paths.DEFAULT_FILE_PATHS import ConfigFilePaths


class DataManager():
    logger = logging.getLogger(__name__)

    def __init__(self) -> None:
        self.config = Config(ConfigFilePaths.data_manager_config)
        self.batch_factory = BatchFactory()
        if self.config.attributes["data_filter"]["use_filter"]:
            self.data_filter = RawDataFilter()
        else:
            self.data_filter = None

    def make_batch(self):
        self.batch_factory.create_batch()
        if self.data_filter:
            self.data_filter.filter(self.batch_factory.batch)
