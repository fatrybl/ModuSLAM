from dataclasses import dataclass, field
from pathlib import Path

from configs.paths.kaist_dataset import KaistDatasetPathConfig as KaistPaths
from configs.sensors.base_sensor_parameters import ParameterConfig
from configs.system.data_manager.batch_factory.datasets.kaist import (
    KaistConfig,
    PairConfig,
)
from configs.system.setup_manager.sensor_factory import SensorConfig
from slam.setup_manager.sensor_factory.sensors import Encoder

DATASET_DIR: Path = Path(__file__).parent / "test_data"


encoder = SensorConfig("encoder", Encoder.__name__, ParameterConfig())

iterable_data_files: list[PairConfig] = field(
    default_factory=lambda: [
        PairConfig(encoder.name, DATASET_DIR / KaistPaths.encoder_data_file),
    ]
)

data_dirs: list[PairConfig] = field(default_factory=lambda: [])


@dataclass
class KaistReaderConfig(KaistConfig):
    directory: Path = DATASET_DIR
    iterable_data_files: list[PairConfig] = iterable_data_files
    data_dirs: list[PairConfig] = data_dirs
