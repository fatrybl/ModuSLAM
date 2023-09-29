from dataclasses import dataclass, field
from pathlib import Path

from configs.system.data_manager.datasets.base_dataset import Dataset


@dataclass
class Pair:
    sensor_name: str
    location: Path


@dataclass
class KaistDataset(Dataset):

    iterable_data_files: list[Pair] = field(metadata={
        'description': 'iterable data files: pairs of (<SENSOR_NAME>, <DATA_PATH>)'})

    data_dirs: list[Pair] = field(metadata={
        'description': 'directory containing data files'})

    data_stamp_file: str = field(default='data_stamp.csv', metadata={
                                 'description': 'file with sorted list of sensor measurements'})
