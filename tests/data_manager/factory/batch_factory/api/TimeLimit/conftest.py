from shutil import rmtree
from typing import Any, Callable, TypeAlias

from hydra import initialize_config_module, compose
from hydra.core.config_store import ConfigStore
from pytest import fixture

from slam.data_manager.factory.batch_factory import BatchFactory
from slam.setup_manager.sensor_factory.sensor_factory import SensorFactory
from tests.data_manager.auxiliary_utils.kaist_data_factory import DataFactory
from tests.data_manager.factory.batch_factory.conftest import CONFIG_MODULE_DIR, BATCH_FACTORY_CONFIG_NAME, \
    SENSOR_FACTORY_CONFIG_NAME
from .config import BFConfig, SFConfig
from .data import (DatasetStructure,
                   data_stamp,
                   stamp_files,
                   csv_data,
                   binary_data,
                   image_data)

Fixture: TypeAlias = Callable[[Any], Any]


@fixture(scope='class')
def kaist_urban_dataset() -> None:
    """
    Generates Kaist Urban Dataset with the predefined data.
    """
    data_factory = DataFactory(dataset_structure=DatasetStructure())
    data_factory.create_dataset_structure()
    data_factory.generate_data(
        data_stamp,
        stamp_files,
        csv_data,
        binary_data,
        image_data)


@fixture(scope='function')
def kaist_batch_factory(kaist_urban_dataset: Fixture) -> BatchFactory:
    cs = ConfigStore.instance()
    cs.store(name=BATCH_FACTORY_CONFIG_NAME, node=BFConfig)

    with initialize_config_module(config_module=CONFIG_MODULE_DIR):
        cfg = compose(config_name=BATCH_FACTORY_CONFIG_NAME)
        return BatchFactory(cfg)


@fixture(scope='function')
def sensor_factory() -> None:
    cs = ConfigStore.instance()
    cs.store(name=SENSOR_FACTORY_CONFIG_NAME, node=SFConfig)
    with initialize_config_module(config_module=CONFIG_MODULE_DIR):
        cfg = compose(config_name=SENSOR_FACTORY_CONFIG_NAME)
        SensorFactory.init_sensors(cfg)


@fixture(scope='class', autouse=True)
def clean():
    yield
    rmtree(DatasetStructure.dataset_directory)
