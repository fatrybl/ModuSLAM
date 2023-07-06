from configs.paths.DEFAULT_FILE_PATHS import ConfigFilePaths
from utils.config import Config
from slam.data_manager.factory.readers.kaist.kaist_reader import KaistReader


class DataReaderFactory():
    def __new__(cls):
        dataset_type = Config(
            ConfigFilePaths.data_manager_config).attributes["data"]["dataset_type"]
        if dataset_type == 'kaist':
            return KaistReader()
        else:
            raise NotImplementedError
