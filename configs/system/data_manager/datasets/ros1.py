from dataclasses import dataclass

from omegaconf import MISSING

from configs.system.data_manager.datasets.base_dataset import DatasetConfig


@dataclass
class Ros1(DatasetConfig):
    """
    Base parameters for any Ros 1 dataset.
    """
    some_params: str = MISSING
