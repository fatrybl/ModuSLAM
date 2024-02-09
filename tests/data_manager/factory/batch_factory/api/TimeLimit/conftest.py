from shutil import rmtree
from typing import cast

from hydra import compose, initialize_config_module
from hydra.core.config_store import ConfigStore
from pytest import fixture

from configs.system.data_manager.batch_factory.batch_factory import BatchFactoryConfig
from configs.system.setup_manager.sensors_factory import SensorFactoryConfig
from slam.setup_manager.sensors_factory.factory import SensorFactory
from tests.data_manager.auxiliary_utils.kaist_data_factory import DataFactory
from tests.data_manager.factory.batch_factory.api.TimeLimit.config import (
    BFConfig,
    SFConfig,
)
from tests.data_manager.factory.batch_factory.api.TimeLimit.data import (
    DatasetStructure,
    binary_data,
    csv_data,
    data_stamp,
    image_data,
    stamp_files,
)
from tests.data_manager.factory.batch_factory.conftest import (
    BATCH_FACTORY_CONFIG_NAME,
    CONFIG_MODULE_DIR,
    SENSOR_FACTORY_CONFIG_NAME,
)


@fixture(scope="class", autouse=True)
def kaist_urban_dataset() -> None:
    """
    Generates custom Kaist Urban Dataset with the predefined data.
    """
    data_factory = DataFactory(dataset_structure=DatasetStructure())
    data_factory.create_dataset_structure()
    data_factory.generate_data(data_stamp, stamp_files, csv_data, binary_data, image_data)


@fixture(scope="class", autouse=True)
def register_configs():
    cs = ConfigStore.instance()
    cs.store(name=BATCH_FACTORY_CONFIG_NAME, node=BFConfig)
    cs.store(name=SENSOR_FACTORY_CONFIG_NAME, node=SFConfig)


@fixture(scope="class", autouse=True)
def sensor_factory(register_configs) -> None:
    with initialize_config_module(version_base=None, config_module=CONFIG_MODULE_DIR):
        cfg: SensorFactoryConfig = cast(SensorFactoryConfig, compose(config_name=SENSOR_FACTORY_CONFIG_NAME))
        SensorFactory.init_sensors(cfg)


@fixture(scope="function")
def batch_factory_cfg(register_configs) -> BatchFactoryConfig:
    with initialize_config_module(version_base=None, config_module=CONFIG_MODULE_DIR):
        cfg: BatchFactoryConfig = cast(BatchFactoryConfig, compose(config_name=BATCH_FACTORY_CONFIG_NAME))
        return cfg


@fixture(scope="class", autouse=True)
def clean():
    yield
    rmtree(DatasetStructure.dataset_directory)
