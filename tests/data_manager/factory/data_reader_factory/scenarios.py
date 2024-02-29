from pathlib import Path

from slam.data_manager.factory.readers.kaist.kaist_reader import KaistReader
from slam.system_configs.system.data_manager.batch_factory.datasets.base_dataset import (
    DatasetConfig,
)
from slam.system_configs.system.data_manager.batch_factory.datasets.kaist.config import (
    KaistConfig,
)
from slam.system_configs.system.data_manager.batch_factory.regime import (
    RegimeConfig,
    Stream,
)
from tests_data.kaist_urban_dataset.data import DATASET_DIR as kaist_dataset_directory

kaist = (
    KaistConfig(directory=kaist_dataset_directory),
    RegimeConfig(name=Stream.name),
    KaistReader,
)

invalid_regime = (
    KaistConfig(directory=kaist_dataset_directory),
    RegimeConfig(name="InvalidRegime"),
)


invalid_dataset = (
    DatasetConfig(
        name="InvalidDataset",
        reader="InvalidReader",
        directory=Path("invalid_path"),
        url="invalid_url",
    ),
    RegimeConfig(name=Stream.name),
)


scenario1 = (*kaist,)
scenario2 = (*invalid_regime,)
scenario3 = (*invalid_dataset,)
