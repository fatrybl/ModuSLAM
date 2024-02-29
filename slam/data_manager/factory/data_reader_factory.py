import logging
from typing import cast

from slam.data_manager.factory.data_reader_ABC import DataReader
from slam.data_manager.factory.readers.kaist.kaist_reader import KaistReader
from slam.system_configs.system.data_manager.batch_factory.datasets.base_dataset import (
    DatasetConfig,
)
from slam.system_configs.system.data_manager.batch_factory.datasets.kaist.config import (
    KaistConfig,
)
from slam.system_configs.system.data_manager.batch_factory.regime import (
    RegimeConfig,
    Stream,
    TimeLimit,
)

logger = logging.getLogger(__name__)


class DataReaderFactory:
    """Factory for creating DataReader instance based on a dataset type."""

    @staticmethod
    def get_reader(dataset_cfg: DatasetConfig, regime_cfg: RegimeConfig) -> DataReader:
        """Creates Data Reader based on dataset type.

        Args:
            regime_cfg (RegimeConfig): configuration of the data flow regime.
            dataset_cfg (DatasetConfig): configuration of the dataset.
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
            case _:
                msg = f"No DataReader exists for dataset type {dataset_cfg.reader!r}."
                logger.critical(msg)
                raise NotImplementedError(msg)
