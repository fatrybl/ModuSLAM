import logging
from typing import cast

from moduslam.data_manager.batch_factory.readers.data_reader_ABC import DataReader
from moduslam.data_manager.batch_factory.readers.kaist.reader import KaistReader
from moduslam.data_manager.batch_factory.readers.tum_vie.reader import TumVieReader
from moduslam.logger.logging_config import data_manager
from moduslam.system_configs.data_manager.batch_factory.datasets.base_dataset import (
    DatasetConfig,
)
from moduslam.system_configs.data_manager.batch_factory.datasets.kaist.config import (
    KaistConfig,
)
from moduslam.system_configs.data_manager.batch_factory.datasets.tum_vie.config import (
    TumVieConfig,
)
from moduslam.system_configs.data_manager.batch_factory.regime import Stream, TimeLimit

logger = logging.getLogger(data_manager)


class DataReaderFactory:
    """Factory for creating DataReader instance based on a dataset type."""

    @staticmethod
    def create(dataset_cfg: DatasetConfig, regime: Stream | TimeLimit) -> DataReader:
        """Creates Data Reader based on dataset type.

        Args:
            dataset_cfg: configuration of the dataset.

            regime: configuration of the data flow regime.

        Raises:
            NotImplementedError: No DataReader exists for the given dataset type.
        """

        match dataset_cfg.reader:
            case KaistReader.__name__:
                dataset_cfg = cast(KaistConfig, dataset_cfg)
                return KaistReader(regime, dataset_cfg)

            case TumVieReader.__name__:
                dataset_cfg = cast(TumVieConfig, dataset_cfg)
                return TumVieReader(regime, dataset_cfg)

            case _:
                msg = f"No DataReader exists for dataset type {dataset_cfg.reader!r}."
                logger.critical(msg)
                raise NotImplementedError(msg)
