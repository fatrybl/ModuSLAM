import logging

from slam.data_manager.factory.batch_factory import BatchFactory
from slam.data_manager.filter.data_filter import RawDataFilter
from slam.data_manager.factory.batch import DataBatch
from slam.utils.config import Config
from configs.paths.DEFAULT_FILE_PATHS import ConfigFilePaths as paths

logger = logging.getLogger(__name__)


class DataManager():

    def __init__(self) -> None:
        self.config = Config.from_file(paths.data_manager_config.value)
        self.batch_factory = BatchFactory()
        logger.info("Data Manager has been configured")

    def make_batch(self):
        self.batch_factory.create_batch()
        logger.info("Data Batch has been created")
        if self.config.attributes["data_filter"]["use_filter"]:
            data_filter = RawDataFilter()
            data_filter.filter(self.batch_factory.batch)
            logger.info("Data Batch has been filtered")

    def make_batch_from_measurements(self, measurements: list) -> DataBatch:
        """
        Interface for getting measurements by other managers.
        Args: list of measurements without data: sensor, file, position in file
        [{"sensor": "camera_rgb_left",
         "location": {"file": Path(),
                      "position": 0},
        {"sensor": "camera_rgb_right",
         "location": {"file": Path(),
                      "position": 0}, 
        ...]
        Returns: DataBatch
        """
        raise NotImplementedError
