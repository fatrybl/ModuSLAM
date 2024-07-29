from dataclasses import dataclass, field

from moduslam.system_configs.data_manager.batch_factory.datasets.base_dataset import (
    DatasetConfig,
)
from moduslam.system_configs.data_manager.batch_factory.regimes import DataRegimeConfig


@dataclass
class BatchFactoryConfig:
    """Batch factory configuration."""

    dataset: DatasetConfig
    regime: DataRegimeConfig
    batch_memory_percent: float = field(
        default=90.0, metadata={"help": "RAM-memory percent used for the data batch."}
    )
