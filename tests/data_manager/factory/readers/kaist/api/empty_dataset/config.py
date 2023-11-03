from dataclasses import dataclass, field
from pathlib import Path


from slam.setup_manager.sensor_factory.sensors import Encoder

from configs.paths.kaist_dataset import KaistDatasetPath as KaistPaths
from configs.system.data_manager.datasets.kaist import KaistConfig, Pair
from configs.system.setup_manager.sensor_factory import SensorConfig
from configs.sensors.base_sensor_parameters import ParameterConfig

from tests.data_manager.factory.readers.kaist.data_factory import DatasetStructure

DATASET_DIR: Path = DatasetStructure.DATASET_DIR


encoder = SensorConfig('encoder', Encoder.__name__, ParameterConfig())

iterable_data_files: list[Pair] = field(default_factory=lambda: [
    Pair(encoder.name, DATASET_DIR / KaistPaths.encoder_data_file),])

data_dirs: list[Pair] = field(default_factory=lambda: [])


@dataclass
class KaistReaderConfig(KaistConfig):
    directory: Path = DATASET_DIR
    iterable_data_files: list[Pair] = iterable_data_files
    data_dirs: list[Pair] = data_dirs
