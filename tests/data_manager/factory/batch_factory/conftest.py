from pathlib import Path
from shutil import rmtree
from typing import Any, Callable, Type, TypeAlias
from pytest import fixture

from hydra import compose, initialize_config_module

# from configs.system.data_manager.batch_factory.datasets.kaist import KaistConfig
# from configs.system.data_manager.batch_factory.regime import RegimeConfig
# from slam.data_manager.factory.readers.kaist.kaist_reader import KaistReader
# from slam.utils.kaist_data_factory import DatasetStructure


CURRENT_DIR: Path = Path(__file__).parent
CONFIG_MODULE_DIR: str = "batch_factory.api.conf"
DATASET_CONFIG_NAME: str = "dataset_config"
REGIME_CONFIG_NAME: str = "regime_config"
SENSOR_CONFIG_NAME: str = "sensor_factory_config"
BATCH_FACTORY_CONFIG_NAME: str = "batch_factory_config"

Fixture: TypeAlias = Callable[[Any], Any]


# @fixture(scope='class')
# def data_reader(dataset_cfg: Type[KaistConfig], regime_cfg: Type[RegimeConfig]) -> KaistReader:
#     return KaistReader(dataset_cfg, regime_cfg)


# @fixture(scope='class')
# def dataset_cfg() -> Type[KaistConfig]:
#     with initialize_config_module(config_module=CONFIG_MODULE_DIR):
#         cfg = compose(config_name=DATASET_CONFIG_NAME)
#         return cfg


# @fixture(scope='class')
# def regime_cfg() -> Type[RegimeConfig]:
#     with initialize_config_module(config_module=CONFIG_MODULE_DIR):
#         cfg = compose(config_name=REGIME_CONFIG_NAME)
#         return cfg


# @fixture(scope='class', autouse=True)
# def clean():
#     yield
#     # rmtree(DatasetStructure.DATASET_DIR)
