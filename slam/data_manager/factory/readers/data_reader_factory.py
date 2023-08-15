import logging
from pathlib import Path
from configs.paths.DEFAULT_FILE_PATHS import ConfigFilePaths
from slam.utils.config import Config
from slam.data_manager.factory.readers.kaist.kaist_reader import KaistReader

logger = logging.getLogger(__name__)


class DataReaderFactory():
    def __new__(cls, config_path: Path = ConfigFilePaths.data_manager_config.value):
        cfg = Config.from_file(config_path)
        try:
            dataset_type = cfg.attributes["data"]["dataset_type"]

        except KeyError:
            logger.critical(
                f'No "data.dataset_type" attribute in config file: {cfg.file_path}')
            raise

        else:
            if dataset_type == 'kaist':
                return KaistReader()
            else:
                logger.critical(
                    f'No DataReader for dataset type: {dataset_type}')
                raise ValueError
