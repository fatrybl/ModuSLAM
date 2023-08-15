from configs.paths.DEFAULT_FILE_PATHS import ConfigFilePaths
from utils.config import Config
from slam.data_manager.factory.readers.kaist.kaist_reader import KaistReader
from slam.data_manager.factory.readers.ros1.ros1_reader import Ros1BagReader

class DataReaderFactory():
    def __new__(cls):
        dataset_type = Config(
            ConfigFilePaths.data_manager_config).attributes["data"]["dataset_type"]
        if dataset_type == 'kaist':
            return KaistReader()
        if dataset_type == 'ros1':
            return Ros1BagReader()
        else:
            raise NotImplementedError
