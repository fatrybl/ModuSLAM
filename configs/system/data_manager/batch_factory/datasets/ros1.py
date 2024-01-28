from dataclasses import dataclass

from configs.system.data_manager.batch_factory.datasets.base_dataset import (
    DatasetConfig,
)


@dataclass
class Ros1Config(DatasetConfig):
    """
    Base parameters for any Ros 1 dataset.
    """

    reader: str = "Ros1Reader"
