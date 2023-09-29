from dataclasses import dataclass

from configs.system.data_manager.datasets.base_dataset import Dataset


@dataclass
class Ros1tDataset(Dataset):
    some_params: str
