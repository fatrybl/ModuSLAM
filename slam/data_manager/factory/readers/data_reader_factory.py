import logging
from typing import Type

from configs.system.data_manager.datasets.base_dataset import Dataset
from slam.data_manager.factory.readers.kaist.kaist_reader import KaistReader

logger = logging.getLogger(__name__)


class DataReaderFactory():
    def __new__(cls, cfg: Type[Dataset]):
        dataset_type: str = cfg.type

        if dataset_type == 'kaist':
            return KaistReader(cfg)

        elif dataset_type == 'ros1':
            raise NotImplementedError

        else:
            logger.critical(
                f'No DataReader for dataset type: {dataset_type}')
            raise ValueError
