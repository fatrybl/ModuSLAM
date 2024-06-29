from pathlib import Path

from moduslam.data_manager.batch_factory.readers.kaist.reader import KaistReader
from moduslam.system_configs.data_manager.batch_factory.datasets.base_dataset import (
    DatasetConfig,
)
from moduslam.system_configs.data_manager.batch_factory.datasets.kaist.config import (
    KaistConfig,
)
from moduslam.system_configs.data_manager.batch_factory.regime import Stream
from tests.conftest import kaist_custom_dataset_dir

kaist_valid = (
    KaistConfig(directory=kaist_custom_dataset_dir),
    Stream(),
    KaistReader,
)

kaist_invalid_dataset = (
    DatasetConfig(
        name="InvalidDataset",
        reader="InvalidReader",
        directory=Path("invalid_path"),
        url="invalid_url",
    ),
    Stream(),
)


scenario1 = (*kaist_valid,)
scenario2 = (*kaist_invalid_dataset,)
