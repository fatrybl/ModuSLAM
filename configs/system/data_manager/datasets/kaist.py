from dataclasses import dataclass, field
from pathlib import Path

from configs.system.data_manager.datasets.base_dataset import Dataset


@dataclass
class Pair:
    sensor_name: str
    location: Path


@dataclass
class KaistDataset(Dataset):

    sensor_data_location: list[Pair] = field(metadata={
        'description': 'pairs of (<SENSOR_NAME>, <DATA_PATH>)'})

    data_stamp_file: str = field(default='data_stamp.csv', metadata={
                                 'description': 'file with sorted list of sensor measurements'})
