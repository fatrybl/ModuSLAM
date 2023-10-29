from shutil import rmtree
from typing import Type
from pytest import fixture

from hydra.core.config_store import ConfigStore
from hydra import compose, initialize_config_module

from slam.data_manager.factory.readers.kaist.kaist_reader import KaistReader
from slam.setup_manager.sensor_factory.sensor_factory import SensorFactory

from configs.system.data_manager.regime import Regime, Stream

from tests.data_manager.factory.readers.kaist.api.one_element_dataset.config_factory import SensorFactoryConfig, KaistReaderConfig
from tests.data_manager.factory.readers.kaist.api.one_element_dataset.data_factory import DataFactory

CONFIG_MODULE_DIR: str = "one_element_dataset.conf"
SENSOR_FACTORY_CONFIG_NAME: str = "sensor_factory_config"
DATASET_CONFIG_NAME: str = "dataset_config"
REGIME_CONFIG_NAME: str = "regime_config"


@fixture(scope='class', autouse=True)
def clean():
    yield
    rmtree(DataFactory.TMP_DIR)


@fixture(scope='class', autouse=True)
def create_dataset() -> None:
    factory = DataFactory()
    factory.generate_data()


@fixture(scope='class', autouse=True)
def register_configs() -> None:
    cs = ConfigStore.instance()
    cs.store(name=SENSOR_FACTORY_CONFIG_NAME, node=SensorFactoryConfig)
    cs.store(name=DATASET_CONFIG_NAME, node=KaistReaderConfig)
    cs.store(name=REGIME_CONFIG_NAME, node=Stream)


@fixture(scope='class')
def sensor_factory_cfg() -> SensorFactoryConfig:
    with initialize_config_module(config_module=CONFIG_MODULE_DIR):
        cfg = compose(config_name=SENSOR_FACTORY_CONFIG_NAME)
        return cfg


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
def sensor_factory(sensor_factory_cfg: SensorFactoryConfig) -> SensorFactory:
    return SensorFactory(sensor_factory_cfg)


@fixture(scope='class')
def data_reader(dataset_cfg: KaistReaderConfig, regime_cfg: Type[Regime]) -> KaistReader:
    return KaistReader(dataset_cfg, regime_cfg)
