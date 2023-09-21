import logging
from pathlib import Path


from configs.paths.DEFAULT_FILE_PATHS import ConfigFilePaths
from slam.utils.config import Config
from slam.data_manager.factory.readers.kaist.kaist_reader import KaistReader
from slam.data_manager.factory.readers.ros1.ros1_reader import Ros1BagReader

# class DataReaderFactory():
#     def __new__(cls):
#         dataset_type = Config(
#             ConfigFilePaths.data_manager_config).attributes["data"]["dataset_type"]
#         if dataset_type == 'kaist':
#             return KaistReader()
#         if dataset_type == 'ros1':
#             return Ros1BagReader()

logger = logging.getLogger(__name__)


class DataReaderFactory():
    def __new__(cls, config_path: Path = ConfigFilePaths.data_manager_config.value):
        cfg = Config.from_file(config_path)
        try:
            dataset_type: str = cfg.attributes["data"]["dataset_type"]

        except KeyError:
            logger.critical(
                f'No "data.dataset_type" attribute in config file: {cfg.file_path}')
            raise

        else:
            if dataset_type == 'kaist':
                return KaistReader()
            if dataset_type == 'ros1':
                return Ros1BagReader()
            else:
                logger.critical(
                    f'No DataReader for dataset type: {dataset_type}')
                raise ValueError
