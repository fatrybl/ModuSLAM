from shutil import rmtree
from typing import Type
from pytest import fixture

from hydra import compose, initialize_config_module

from configs.system.data_manager.datasets.kaist import KaistConfig
from configs.system.data_manager.regime import Regime
from slam.data_manager.factory.readers.kaist.kaist_reader import KaistReader
from .data_factory import DatasetStructure

CONFIG_MODULE_DIR: str = "api.conf"
DATASET_CONFIG_NAME: str = "dataset_config"
REGIME_CONFIG_NAME: str = "regime_config"
SENSOR_CONFIG_NAME: str = "sensor_factory_config"


@fixture(scope='class')
def dataset_cfg() -> Type[KaistConfig]:
    with initialize_config_module(config_module=CONFIG_MODULE_DIR):
        cfg = compose(config_name=DATASET_CONFIG_NAME)
        return cfg


@fixture(scope='class')
def regime_cfg() -> Type[Regime]:
    with initialize_config_module(config_module=CONFIG_MODULE_DIR):
        cfg = compose(config_name=REGIME_CONFIG_NAME)
        return cfg


@fixture(scope='class')
def data_reader(dataset_cfg: Type[KaistConfig], regime_cfg: Type[Regime]) -> KaistReader:
    return KaistReader(dataset_cfg, regime_cfg)


@fixture(scope='class', autouse=True)
def clean():
    yield
    rmtree(DatasetStructure.DATASET_DIR)
