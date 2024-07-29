import logging
from typing import cast

from moduslam.data_manager.batch_factory.readers.data_reader_ABC import DataReader
from moduslam.data_manager.batch_factory.readers.kaist.reader import KaistReader
from moduslam.data_manager.batch_factory.readers.tum_vie.reader import TumVieReader
from moduslam.logger.logging_config import data_manager
from moduslam.system_configs.data_manager.batch_factory.data_readers import DataReaders
from moduslam.system_configs.data_manager.batch_factory.datasets.base_dataset import (
    DatasetConfig,
)
from moduslam.system_configs.data_manager.batch_factory.datasets.kaist.config import (
    KaistConfig,
)
from moduslam.system_configs.data_manager.batch_factory.datasets.tum_vie.config import (
    TumVieConfig,
)
from moduslam.system_configs.data_manager.batch_factory.regimes import (
    DataRegimeConfig,
    Stream,
    TimeLimit,
)

logger = logging.getLogger(data_manager)


class DataReaderFactory:
    """Factory for creating DataReader instance based on a dataset type."""

    @staticmethod
    def create(dataset_config: DatasetConfig, regime_config: DataRegimeConfig) -> DataReader:
        """Creates Data Reader based on dataset type.

        Args:
            dataset_config: configuration of the dataset.

            regime_config: configuration of the data flow regime.

        Raises:
            NotImplementedError: No DataReader exists for the given dataset type.

            ValueError: Invalid regime name.
        """
        regime: Stream | TimeLimit
        match regime_config.name:
            case Stream.name:
                regime = Stream()

            case TimeLimit.name:
                regime = TimeLimit(regime_config.start, regime_config.stop)

            case _:
                msg = f"Invalid regime name {regime_config.name!r}."
                logger.critical(msg)
                raise ValueError(msg)

        match dataset_config.reader:
            case DataReaders.kaist_reader:
                dataset_config = cast(KaistConfig, dataset_config)
                return KaistReader(regime, dataset_config)

            case DataReaders.tum_vie_reader:
                dataset_config = cast(TumVieConfig, dataset_config)
                return TumVieReader(regime, dataset_config)

            case _:
                msg = f"No DataReader exists for dataset type {dataset_config.reader!r}."
                logger.critical(msg)
                raise NotImplementedError(msg)
