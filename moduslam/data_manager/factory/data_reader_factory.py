import logging
from typing import cast

from moduslam.data_manager.factory.data_reader_ABC import DataReader
from moduslam.data_manager.factory.readers.kaist.kaist_reader import KaistReader
from moduslam.data_manager.factory.readers.ros2.ros2_reader import Ros2DataReader
from moduslam.logger.logging_config import data_manager
from moduslam.system_configs.data_manager.batch_factory.datasets.base_dataset import (
    DatasetConfig,
)
from moduslam.system_configs.data_manager.batch_factory.datasets.kaist.config import (
    KaistConfig,
)
from moduslam.system_configs.data_manager.batch_factory.datasets.ros2.config import (
    Ros2Config,
)
from moduslam.system_configs.data_manager.batch_factory.regime import (
    RegimeConfig,
    Stream,
    TimeLimit,
)

logger = logging.getLogger(data_manager)


class DataReaderFactory:
    """Factory for creating DataReader instance based on a dataset type."""

    @staticmethod
    def create_reader(dataset_cfg: DatasetConfig, regime_cfg: RegimeConfig) -> DataReader:
        """Creates Data Reader based on dataset type.

        Args:
            dataset_cfg (DatasetConfig): configuration of the dataset.

            regime_cfg (RegimeConfig): configuration of the data flow regime.

        Raises:
            ValueError: Invalid regime name.

            NotImplementedError: No DataReader exists for the given dataset type.
        """
        regime: Stream | TimeLimit

        match regime_cfg.name:
            case TimeLimit.name:
                regime = TimeLimit(start=regime_cfg.start, stop=regime_cfg.stop)
            case Stream.name:
                regime = Stream()
            case _:
                msg = f"Invalid regime: {regime_cfg.name!r}."
                logger.critical(msg)
                raise ValueError(msg)

        match dataset_cfg.reader:
            case KaistReader.__name__:
                dataset_cfg = cast(KaistConfig, dataset_cfg)
                return KaistReader(regime, dataset_cfg)
            # TODO: Add ROS2 reader here.
            case Ros2DataReader.__name__:
                dataset_cfg = cast(Ros2Config)
            case _:
                msg = f"No DataReader exists for dataset type {dataset_cfg.reader!r}."
                logger.critical(msg)
                raise NotImplementedError(msg)
