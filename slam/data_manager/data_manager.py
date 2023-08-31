import logging

from plum import dispatch

from slam.data_manager.factory.batch_factory import BatchFactory
from slam.data_manager.filter.data_filter import RawDataFilter
from slam.utils.config import Config
from slam.data_manager.factory.readers.element_factory import Element
from configs.paths.DEFAULT_FILE_PATHS import ConfigFilePaths as paths
from slam.utils.meta_singleton import MetaSingleton

logger = logging.getLogger(__name__)


class DataManager(metaclass=MetaSingleton):

    def __init__(self) -> None:
        self.config = Config.from_file(paths.data_manager_config.value)
        self.batch_factory = BatchFactory()
        logger.info("Data Manager has been configured")

    @dispatch
    def make_batch(self) -> None:
        self.batch_factory.create_batch()
        logger.info("Data Batch has been created")
        if self.config.attributes["data_filter"]["use_filter"]:
            data_filter = RawDataFilter()
            data_filter.filter(self.batch_factory.batch)
            logger.info("Data Batch has been filtered")

    @dispatch
    def make_batch(self, measurements: list[Element | dict]) -> None:
        """
        Interface for getting row data from measurements.
        Args: 
            measurements:
                 list of Elements or dicts 
        """
        self.batch_factory.save_current_state()
        self.batch_factory.create_batch(measurements)
