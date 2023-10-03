import logging
from typing import Type

from configs.system.data_manager.datasets.base_dataset import Dataset
from configs.system.data_manager.datasets.kaist import Kaist
from configs.system.data_manager.datasets.ros1 import Ros1
from slam.data_manager.factory.readers.kaist.kaist_reader import KaistReader

logger = logging.getLogger(__name__)


class DataReaderFactory():
    def __new__(cls, cfg: Type[Dataset]):
        if cfg.dataset_type == Kaist.__name__:
            return KaistReader(cfg)

        elif cfg.dataset_type == Ros1.__name__:
            raise NotImplementedError

        else:
            logger.critical(
                f'No DataReader for dataset type: {dataset_type}')
            raise TypeError
