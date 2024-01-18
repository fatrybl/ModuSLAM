from shutil import rmtree
from typing import Any, Callable, TypeAlias

from hydra import compose, initialize_config_module
from hydra.core.config_store import ConfigStore
from pytest import fixture

from slam.data_manager.factory.batch_factory import BatchFactory
from tests.data_manager.auxiliary_utils.kaist_data_factory import DataFactory
from tests.data_manager.factory.batch_factory.conftest import (
    BATCH_FACTORY_CONFIG_NAME,
    CONFIG_MODULE_DIR,
)
from .config import BFConfig
from .data import (
    DatasetStructure,
    binary_data,
    csv_data,
    data_stamp,
    image_data,
    stamp_files,
)

Fixture: TypeAlias = Callable[[Any], Any]


@fixture(scope="class")
def kaist_urban_dataset() -> None:
    """
    Generates Kaist Urban Dataset with the predefined data.
    """
    data_factory = DataFactory(dataset_structure=DatasetStructure())
    data_factory.create_dataset_structure()
    data_factory.generate_data(data_stamp, stamp_files, csv_data, binary_data, image_data)


@fixture(scope="function")
def kaist_batch_factory(kaist_urban_dataset: Fixture) -> BatchFactory:
    cs = ConfigStore.instance()
    cs.store(name=BATCH_FACTORY_CONFIG_NAME, node=BFConfig)

    with initialize_config_module(config_module=CONFIG_MODULE_DIR):
        cfg = compose(config_name=BATCH_FACTORY_CONFIG_NAME)
        return BatchFactory(cfg)


@fixture(scope="class", autouse=True)
def clean():
    yield
    rmtree(DatasetStructure.dataset_directory)
