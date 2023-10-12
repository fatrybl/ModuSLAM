from dataclasses import dataclass

from omegaconf import MISSING

from configs.system.data_manager.datasets.base_dataset import Dataset


@dataclass
class Ros1(Dataset):
    dataset_type: str = 'ros1'