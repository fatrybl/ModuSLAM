import logging

from configs.system.data_manager.datasets.kaist import KaistConfig
from slam.data_manager.factory.readers.kaist.kaist_reader import KaistReader

logger = logging.getLogger(__name__)


class DataReaderFactory():
    """
    Factory for creating DataReader instance based on dataset type.
    """

    def __init__(self, dataset_type: str) -> None:
        if dataset_type == KaistConfig.__name__:
            self.data_reader = KaistReader
        else:
            msg = f"No DataReader exists for dataset type {dataset_type}."
            logger.critical(msg)
            raise NotImplementedError(msg)
