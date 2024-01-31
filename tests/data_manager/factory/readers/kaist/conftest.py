from typing import Any, Callable, TypeAlias, cast

from hydra import compose, initialize_config_module
from pytest import fixture

from configs.system.data_manager.batch_factory.datasets.kaist import KaistConfig
from configs.system.data_manager.batch_factory.regime import RegimeConfig
from slam.data_manager.factory.readers.kaist.kaist_reader import KaistReader

CONFIG_MODULE_DIR: str = "conf"
DATASET_CONFIG_NAME: str = "dataset_config"
REGIME_CONFIG_NAME: str = "regime_config"
SENSOR_FACTORY_CONFIG_NAME: str = "sensor_factory_config"

Fixture: TypeAlias = Callable[[Any], Any]


@fixture(scope="class")
def dataset_cfg() -> KaistConfig:
    with initialize_config_module(version_base=None, config_module=CONFIG_MODULE_DIR):
        cfg: KaistConfig = cast(KaistConfig, compose(config_name=DATASET_CONFIG_NAME))
        return cfg


@fixture(scope="class")
def regime_cfg() -> RegimeConfig:
    with initialize_config_module(version_base=None, config_module=CONFIG_MODULE_DIR):
        cfg: RegimeConfig = cast(RegimeConfig, compose(config_name=REGIME_CONFIG_NAME))
        return cfg


@fixture(scope="class")
def data_reader(dataset_cfg: KaistConfig, regime_cfg: RegimeConfig) -> KaistReader:
    return KaistReader(dataset_cfg, regime_cfg)
