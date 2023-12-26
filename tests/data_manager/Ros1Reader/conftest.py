# from pytest import fixture
# from shutil import rmtree
from tests.data_manager.factory.readers.ros1.data_factory import TestDataFactory
# from slam.setup_manager.sensor_factory.sensor_factory import SensorFactory
from configs.experiments.ros1.config import SF
# from pathlib import Path


from shutil import rmtree
from typing import Type
from pytest import fixture

from hydra.core.config_store import ConfigStore
from hydra import compose, initialize_config_module

from slam.data_manager.factory.readers.kaist.kaist_reader import KaistReader
from slam.setup_manager.sensor_factory.sensor_factory import SensorFactory
from slam.setup_manager.sensor_factory.sensors import (
    Sensor)
from configs.system.data_manager.regime import Regime, Stream

from tests.data_manager.factory.readers.kaist.api.config_factory import SensorFactoryConfig, KaistReaderConfig
from tests.data_manager.factory.readers.kaist.api.data_factory import DataFactory

CONFIG_MODULE_DIR: str = "ros1.api.conf"
SENSOR_FACTORY_CONFIG_NAME: str = "sensor_factory_config"
DATASET_CONFIG_NAME: str = "dataset_config"
REGIME_CONFIG_NAME: str = "regime_config"
SENSOR_CONFIG_NAME: str = "sensor_config"

@fixture(scope='module', autouse=True)
def register_configs() -> None:
    cs = ConfigStore.instance()
    cs.store(name=SENSOR_FACTORY_CONFIG_NAME, node=SensorFactoryConfig)
    cs.store(name=DATASET_CONFIG_NAME, node=KaistReaderConfig)
    cs.store(name=REGIME_CONFIG_NAME, node=Stream)
    # cs.store(name=SENSOR_CONFIG_NAME, node=Sensor)


@fixture(scope='module')
def sensor_factory_cfg() -> SensorFactoryConfig:
    with initialize_config_module(config_module=CONFIG_MODULE_DIR):
        cfg = compose(config_name=SENSOR_FACTORY_CONFIG_NAME)
        return cfg

@fixture(scope='module', autouse=True)
def prepare_data():
    data_factory = TestDataFactory()
    data_factory.prepare_data()
    # cfg = SF()
    # SensorFactory(cfg)
    yield

@fixture(scope='class')
def sensor_factory(sensor_factory_cfg: SensorFactoryConfig) -> SensorFactory:
    return SensorFactory(sensor_factory_cfg)


@fixture(scope='module', autouse=True)
def clean():
    yield
    rmtree(TestDataFactory.DATA_PATH_FOLDER.name)
    TestDataFactory.MASTER_FILE_PATH.unlink()



