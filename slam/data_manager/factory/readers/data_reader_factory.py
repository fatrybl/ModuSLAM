import logging

from configs.system.data_manager.datasets.kaist import Kaist
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

    def __init__(self, dataset_type: str) -> None:
        if dataset_type == Kaist.__name__:
            self.data_reader = KaistReader

        if dataset_type == Kaist.__name__:
            self.data_reader = Ros1BagReader
        else:
            msg = f"No DataReader exists for dataset type {dataset_type}."
            logger.critical(msg)
            raise NotImplementedError(msg)

