from pathlib import Path

from phd.moduslam.data_manager.batch_factory.configs import (
    DataRegimeConfig,
    DatasetConfig,
)
from phd.moduslam.data_manager.batch_factory.readers.kaist.configs.base import (
    KaistConfig,
)
from phd.moduslam.data_manager.batch_factory.readers.kaist.reader import KaistReader
from phd.moduslam.data_manager.batch_factory.readers.tum_vie.configs.base import (
    TumVieConfig,
)
from phd.moduslam.data_manager.batch_factory.readers.tum_vie.reader import TumVieReader
from phd.moduslam.data_manager.batch_factory.regimes import Stream, TimeLimit
from phd.moduslam.sensors_factory.configs import SensorConfig
from phd.tests.conftest import kaist_custom_dataset_dir, tum_vie_dataset_dir

sensor_factory_kaist = {"encoder": SensorConfig("encoder")}
sensor_factory_tum_vie = {"stereo": SensorConfig("stereo")}

valid_regime_config1 = DataRegimeConfig(name=Stream.name)
valid_regime_config2 = DataRegimeConfig(name=TimeLimit.name, start="0", stop="1")
valid_regime_config3 = DataRegimeConfig(
    name=Stream.name, start="0.0", stop="1.226649075999999885e+06"  # 1-st image from test data
)
invalid_regime_config = DataRegimeConfig(name="InvalidRegime")

kaist_cfg = KaistConfig(directory=kaist_custom_dataset_dir)
tum_vie_cfg = TumVieConfig(directory=tum_vie_dataset_dir)

kaist = (
    (kaist_cfg, valid_regime_config1, sensor_factory_kaist, KaistReader),
    (kaist_cfg, valid_regime_config2, sensor_factory_kaist, KaistReader),
)

tum_vie = (
    (tum_vie_cfg, valid_regime_config1, sensor_factory_tum_vie, TumVieReader),
    (tum_vie_cfg, valid_regime_config3, sensor_factory_tum_vie, TumVieReader),
)


valid_readers = (*kaist, *tum_vie)

invalid_dataset = (
    DatasetConfig(
        name="InvalidDataset",
        reader="InvalidReader",
        directory=Path("invalid_path"),
        url="invalid_url",
    ),
    valid_regime_config1,
)
invalid_regime = (
    KaistConfig(directory=kaist_custom_dataset_dir),
    invalid_regime_config,
)
