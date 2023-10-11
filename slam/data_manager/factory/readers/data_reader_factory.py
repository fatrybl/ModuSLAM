import logging
from typing import Type

from configs.system.data_manager.datasets.base_dataset import Dataset
from configs.system.data_manager.datasets.kaist import Kaist
from configs.system.data_manager.datasets.ros1 import Ros1
from configs.system.data_manager.manager import Regime
from slam.data_manager.factory.readers.data_reader import DataReader
from slam.data_manager.factory.readers.kaist.kaist_reader import KaistReader

logger = logging.getLogger(__name__)


class DataReaderFactory():
    def __new__(cls, dataset_params: Type[Dataset], regime_params: type[Regime]) -> Type[DataReader]:
        if dataset_params.dataset_type == Kaist.__name__:
            return KaistReader(dataset_params, regime_params)

        elif dataset_params.dataset_type == Ros1.__name__:
            raise NotImplementedError

        else:
            logger.critical(
                f'No DataReader for dataset type: {dataset_params.dataset_type}')
            raise TypeError
