from dataclasses import dataclass

from omegaconf import MISSING

from configs.system.data_manager.datasets.base_dataset import Dataset


@dataclass
class Ros1(Dataset):
    """
    Base parameters for any Ros 1 dataset.
    """
    some_params: str = MISSING
