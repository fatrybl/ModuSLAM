from dataclasses import dataclass, field
from pathlib import Path

from omegaconf import MISSING

from configs.system.data_manager.datasets.base_dataset import Dataset


@dataclass
class Pair:
    """
    Pair of unique sensor name and sensor`s data location.
    """
    sensor_name: str
    location: Path


@dataclass
class Kaist(Dataset):
    """
    Kaist Urban Dataset parameters.
    """

    type: str = 'Kaist'

    name: str = 'Kaist Urban Dataset'

    url: str = 'https://sites.google.com/view/complex-urban-dataset'

    data_stamp_file: Path = field(
        metadata={'description': 'file with sorted list of sensor measurements'}, default_factory=MISSING)

    iterable_data_files: list[Pair] = field(metadata={
        'description': 'iterable data files: pairs of (<SENSOR_NAME>, <DATA_PATH>)'}, default_factory=MISSING)

    data_dirs: list[Pair] = field(metadata={
        'description': 'directories containing data files'}, default_factory=MISSING)
