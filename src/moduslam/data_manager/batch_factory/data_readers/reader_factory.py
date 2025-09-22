import logging
from typing import cast

from moduslam.data_manager.batch_factory.configs import (
    DataReaders,
    DataRegimeConfig,
    DatasetConfig,
)
from moduslam.data_manager.batch_factory.data_readers.kaist.configs.base import (
    KaistConfig,
)
from moduslam.data_manager.batch_factory.data_readers.kaist.reader import (
    KaistReader,
)
from moduslam.data_manager.batch_factory.data_readers.reader_ABC import DataReader
from moduslam.data_manager.batch_factory.data_readers.regime_factory import (
    kaist_regime,
    ros2_regime,
    tum_vie_regime,
)
from moduslam.data_manager.batch_factory.data_readers.ros2.configs.base import (
    Ros2Config,
)
from moduslam.data_manager.batch_factory.data_readers.ros2.reader import Ros2Reader
from moduslam.data_manager.batch_factory.data_readers.tum_vie.configs.base import (
    TumVieConfig,
)
from moduslam.data_manager.batch_factory.data_readers.tum_vie.reader import (
    TumVieReader,
)
from moduslam.data_manager.batch_factory.regimes import Stream, TimeLimit
from moduslam.logger.logging_config import data_manager

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
        case DataReaders.kaist_urban:
            try:
                regime = kaist_regime(regime_config)
            except ValueError as e:
                logger.critical(e)
                raise

            dataset_config = cast(KaistConfig, dataset_config)
            return KaistReader(dataset_config), regime

        case DataReaders.tum_vie:
            try:
                regime = tum_vie_regime(regime_config)
            except ValueError as e:
                logger.critical(e)
                raise

            dataset_config = cast(TumVieConfig, dataset_config)
            return TumVieReader(dataset_config), regime

        case DataReaders.ros2:
            try:
                regime = ros2_regime(regime_config)
            except ValueError as e:
                logger.critical(e)
                raise

            dataset_config = cast(Ros2Config, dataset_config)
            return Ros2Reader(dataset_config), regime

        case _:
            msg = f"No DataReader exists for the dataset type {dataset_config.reader!r}."
            logger.critical(msg)
            raise NotImplementedError(msg)
