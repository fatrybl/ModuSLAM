import logging
from typing import Type

from configs.system.data_manager.datasets.base_dataset import Dataset
from configs.system.data_manager.datasets.kaist import Kaist
from configs.system.data_manager.datasets.ros1 import Ros1
from configs.system.data_manager.manager import Regime
from slam.data_manager.factory.readers.data_reader import DataReader
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
    def __new__(cls, dataset_params: Type[Dataset], regime_params: type[Regime]) -> Type[DataReader]:
        if dataset_params.dataset_type == Kaist.__name__:
            return KaistReader(dataset_params, regime_params)

        elif dataset_params.dataset_type == Ros1.__name__:
            return Ros1BagReader(dataset_params, regime_params)

        else:
            logger.critical(
                f'No DataReader for dataset type: {dataset_params.dataset_type}')
            raise TypeError

