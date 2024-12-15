import logging
from typing import cast

from phd.logger.logging_config import data_manager
from phd.moduslam.data_manager.batch_factory.configs import (
    DataReaders,
    DataRegimeConfig,
    DatasetConfig,
)
from phd.moduslam.data_manager.batch_factory.readers.kaist.configs.base import (
    KaistConfig,
)
from phd.moduslam.data_manager.batch_factory.readers.kaist.reader import KaistReader
from phd.moduslam.data_manager.batch_factory.readers.reader_ABC import DataReader
from phd.moduslam.data_manager.batch_factory.readers.regime_factory import Factory
from phd.moduslam.data_manager.batch_factory.readers.tum_vie.configs.base import (
    TumVieConfig,
)
from phd.moduslam.data_manager.batch_factory.readers.tum_vie.reader import TumVieReader

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

            ValueError: if a regime name in config is invalid.
        """

        match dataset_config.reader:
            case DataReaders.kaist_reader:
                try:
                    regime = Factory.kaist_regime(regime_config)
                except ValueError as e:
                    logger.critical(e)
                    raise

                dataset_config = cast(KaistConfig, dataset_config)
                return KaistReader(regime, dataset_config)

            case DataReaders.tum_vie_reader:
                try:
                    regime = Factory.tum_vie_regime(regime_config)
                except ValueError as e:
                    logger.critical(e)
                    raise

                dataset_config = cast(TumVieConfig, dataset_config)
                return TumVieReader(regime, dataset_config)

            case _:
                msg = f"No DataReader exists for the dataset type {dataset_config.reader!r}."
                logger.critical(msg)
                raise NotImplementedError(msg)
