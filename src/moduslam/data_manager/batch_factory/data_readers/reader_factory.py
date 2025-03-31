import logging
from typing import cast

from src.logger.logging_config import data_manager
from src.moduslam.data_manager.batch_factory.configs import (
    DataReaders,
    DataRegimeConfig,
    DatasetConfig,
)
from src.moduslam.data_manager.batch_factory.data_readers.kaist.configs.base import (
    KaistConfig,
)
from src.moduslam.data_manager.batch_factory.data_readers.kaist.reader import (
    KaistReader,
)
from src.moduslam.data_manager.batch_factory.data_readers.reader_ABC import DataReader
from src.moduslam.data_manager.batch_factory.data_readers.regime_factory import Factory
from src.moduslam.data_manager.batch_factory.data_readers.tum_vie.configs.base import (
    TumVieConfig,
)
from src.moduslam.data_manager.batch_factory.data_readers.tum_vie.reader import (
    TumVieReader,
)
from src.moduslam.data_manager.batch_factory.regimes import Stream, TimeLimit

logger = logging.getLogger(data_manager)


def create(
    dataset_config: DatasetConfig, regime_config: DataRegimeConfig
) -> tuple[DataReader, Stream | TimeLimit]:
    """Creates Data Reader and regime.

    Args:
        dataset_config: configuration for the dataset.

        regime_config: configuration for the data collection regime.

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
            return KaistReader(dataset_config), regime

        case DataReaders.tum_vie_reader:
            try:
                regime = Factory.tum_vie_regime(regime_config)
            except ValueError as e:
                logger.critical(e)
                raise

            dataset_config = cast(TumVieConfig, dataset_config)
            return TumVieReader(dataset_config), regime

        case _:
            msg = f"No DataReader exists for the dataset type {dataset_config.reader!r}."
            logger.critical(msg)
            raise NotImplementedError(msg)
