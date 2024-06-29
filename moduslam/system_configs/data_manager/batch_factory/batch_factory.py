from dataclasses import dataclass

from moduslam.system_configs.data_manager.batch_factory.datasets.base_dataset import (
    DatasetConfig,
)
from moduslam.system_configs.data_manager.batch_factory.regime import Stream, TimeLimit


@dataclass
class BatchFactoryConfig:
    """Batch factory configuration."""

    dataset: DatasetConfig
    regime: Stream | TimeLimit
    batch_memory_percent: float = 50.0
