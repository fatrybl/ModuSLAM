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
    """Factory for creating DataReader instance based on supported datasets.

    Returns:
        Type[DataReader]: data reader for a dataset.
    """

    def __new__(cls, dataset_params: Type[Dataset], regime_params: type[Regime]) -> Type[DataReader]:
        """Creates data reader for a given dataset.

        Args:
            dataset_params (Type[Dataset]): params of a dataset.
            regime_params (type[Regime]): params of a data flow regime: Stream or TimeRange. 

        Raises:
            NotImplementedError: no data reader for a given dataset.

        Returns:
            Type[DataReader]: data reader object for a given dataset.
        """
        if dataset_params.dataset_type == Kaist.__name__:
            return KaistReader(dataset_params, regime_params)

        else:
            logger.critical(
                f'No DataReader for dataset type: {dataset_params.dataset_type}')
            raise NotImplementedError
