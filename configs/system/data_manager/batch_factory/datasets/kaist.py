from dataclasses import dataclass, field
from pathlib import Path

from omegaconf import MISSING

from configs.paths.kaist_dataset import KaistDatasetPathConfig
from configs.system.data_manager.batch_factory.datasets.base_dataset import DatasetConfig


@dataclass
class PairConfig:
    """
    Pair of unique sensor name and sensor data location.
    """
    sensor_name: str
    location: Path


@dataclass
class KaistConfig(DatasetConfig):
    """
    Kaist Urban Dataset parameters.
    """

    type: str = 'Kaist'

    name: str = 'Kaist Urban Dataset'

    url: str = 'https://sites.google.com/view/complex-urban-dataset'

    paths: KaistDatasetPathConfig = field(
        default_factory=KaistDatasetPathConfig,
        metadata={'description': 'relative paths of Kaist Urban Dataset files & directories'})

    iterable_data_files: list[PairConfig] = field(metadata={
        'description': 'iterable data files: pairs of (<SENSOR_NAME>, <DATA_PATH>)'}, default_factory=MISSING)

    data_dirs: list[PairConfig] = field(metadata={
        'description': 'directories containing data files'}, default_factory=MISSING)
