from pathlib import Path

from moduslam.data_manager.batch_factory.readers.kaist.reader import KaistReader
from moduslam.data_manager.batch_factory.readers.tum_vie.reader import TumVieReader
from moduslam.system_configs.data_manager.batch_factory.datasets.base_dataset import (
    DatasetConfig,
)
from moduslam.system_configs.data_manager.batch_factory.datasets.kaist.config import (
    KaistConfig,
)
from moduslam.system_configs.data_manager.batch_factory.datasets.tum_vie.config import (
    TumVieConfig,
)
from moduslam.system_configs.data_manager.batch_factory.regimes import (
    DataRegimeConfig,
    Stream,
    TimeLimit,
)
from tests.conftest import kaist_custom_dataset_dir, tum_vie_dataset_dir

_valid_regime_config1 = DataRegimeConfig(name=Stream.name)
_valid_regime_config2 = DataRegimeConfig(name=TimeLimit.name, start=0, stop=0)
_invalid_regime_config = DataRegimeConfig(name="InvalidRegime")

_kaist = (
    (KaistConfig(directory=kaist_custom_dataset_dir), _valid_regime_config1, KaistReader),
    (KaistConfig(directory=kaist_custom_dataset_dir), _valid_regime_config2, KaistReader),
)

_tum_vie = (
    (TumVieConfig(directory=tum_vie_dataset_dir), _valid_regime_config1, TumVieReader),
    (TumVieConfig(directory=tum_vie_dataset_dir), _valid_regime_config2, TumVieReader),
)


valid_readers = (*_kaist, *_tum_vie)

invalid_dataset = (
    DatasetConfig(
        name="InvalidDataset",
        reader="InvalidReader",
        directory=Path("invalid_path"),
        url="invalid_url",
    ),
    _valid_regime_config1,
)
invalid_regime = (
    KaistConfig(directory=kaist_custom_dataset_dir),
    _invalid_regime_config,
)
