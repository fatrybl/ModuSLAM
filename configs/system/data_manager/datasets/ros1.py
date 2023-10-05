from dataclasses import dataclass

from omegaconf import MISSING

from configs.system.data_manager.datasets.base_dataset import Dataset


@dataclass
class Ros1(Dataset):
    some_params: str = MISSING
