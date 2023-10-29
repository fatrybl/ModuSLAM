from shutil import rmtree
from typing import Type
from pytest import fixture

from hydra.core.config_store import ConfigStore
from hydra import compose, initialize_config_module

from slam.data_manager.factory.readers.kaist.kaist_reader import KaistReader

from configs.system.data_manager.regime import Regime, Stream

from .config import (
    KaistReaderConfig,
    TMP_DIR, DATASET_CONFIG_NAME, REGIME_CONFIG_NAME, CONFIG_MODULE_DIR)
from .data_factory import DataFactory


@fixture(scope='class', autouse=True)
def register_configs() -> None:
    cs = ConfigStore.instance()
    cs.store(name=DATASET_CONFIG_NAME, node=KaistReaderConfig)
    cs.store(name=REGIME_CONFIG_NAME, node=Stream)


@fixture(scope='class', autouse=True)
def create_dataset() -> None:
    factory = DataFactory()
    factory.generate_data()


@fixture(scope='class')
def dataset_cfg() -> KaistReaderConfig:
    with initialize_config_module(config_module=CONFIG_MODULE_DIR):
        cfg = compose(config_name=DATASET_CONFIG_NAME)
        return cfg


@fixture(scope='class')
def regime_cfg() -> Type[Regime]:
    with initialize_config_module(config_module=CONFIG_MODULE_DIR):
        cfg = compose(config_name=REGIME_CONFIG_NAME)
        return cfg


@fixture(scope='class')
def data_reader(dataset_cfg: KaistReaderConfig, regime_cfg: Type[Regime]) -> KaistReader:
    return KaistReader(dataset_cfg, regime_cfg)


@fixture(scope='class', autouse=True)
def clean():
    yield
    rmtree(TMP_DIR)
