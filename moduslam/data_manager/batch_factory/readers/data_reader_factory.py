import logging
from typing import cast

from moduslam.data_manager.batch_factory.readers.data_reader_ABC import DataReader
from moduslam.data_manager.batch_factory.readers.kaist.reader import KaistReader
from moduslam.data_manager.batch_factory.readers.regime_factory import Factory
from moduslam.data_manager.batch_factory.readers.ros2.reader import Ros2DataReader
from moduslam.data_manager.batch_factory.readers.tum_vie.reader import TumVieReader
from moduslam.logger.logging_config import data_manager
from moduslam.system_configs.data_manager.batch_factory.data_readers import DataReaders
from moduslam.system_configs.data_manager.batch_factory.datasets.base_dataset import (
    DatasetConfig,
)
from moduslam.system_configs.data_manager.batch_factory.datasets.kaist.config import (
    KaistConfig,
)
from moduslam.system_configs.data_manager.batch_factory.datasets.ros2.config import (
    Ros2Config,
)
from moduslam.system_configs.data_manager.batch_factory.datasets.tum_vie.config import (
    TumVieConfig,
)
from moduslam.system_configs.data_manager.batch_factory.regimes import DataRegimeConfig

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
        """

        match dataset_config.reader:
            case DataReaders.kaist_reader:
                regime = Factory.kaist_regime(regime_config)
                dataset_config = cast(KaistConfig, dataset_config)
                return KaistReader(regime, dataset_config)

            case DataReaders.tum_vie_reader:
                regime = Factory.tum_vie_regime(regime_config)
                dataset_config = cast(TumVieConfig, dataset_config)
                return TumVieReader(regime, dataset_config)

            case DataReaders.ros2_reader:
                regime = Factory.ros2_regime(regime_config)
                dataset_config = cast(Ros2Config, dataset_config)
                logger.debug("Creating Ros2DataReader111111111111111111111111111111111111111111111111111111111...")
                return Ros2DataReader(regime, dataset_config)

            case _:
                msg = f"No DataReader exists for dataset type {dataset_config.reader!r}."
                logger.critical(msg)
                raise NotImplementedError(msg)
