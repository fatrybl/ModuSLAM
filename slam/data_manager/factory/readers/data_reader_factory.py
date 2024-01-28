import logging

from slam.data_manager.factory.readers.data_reader_ABC import DataReader
from slam.data_manager.factory.readers.kaist.kaist_reader import KaistReader

logger = logging.getLogger(__name__)


class DataReaderFactory:
    """
    Factory for creating DataReader instance based on dataset type.
    """

    @staticmethod
    def get_reader(data_reader_name: str) -> type[DataReader]:
        """
        Creates Data Reader based on dataset type.

        TODO:
            1) Remove string comparison of Reader type.
            2) Refactor type annotations for configs.


        Args:
            data_reader_name (str): name of the DataReader class.

        Raises:
            NotImplementedError: No DataReader exists for the given dataset type.
        """
        match data_reader_name:
            case "KaistReader":
                return KaistReader
            case _:
                msg = f"No DataReader exists for dataset type {data_reader_name!r}."
                logger.critical(msg)
                raise NotImplementedError(msg)
