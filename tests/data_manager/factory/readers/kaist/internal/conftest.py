from shutil import rmtree
from pytest import fixture

from hydra.core.config_store import ConfigStore

from tests.data_manager.auxiliary_utils.kaist_data_factory import DataFactory

from configs.system.data_manager.batch_factory.regime import StreamConfig

from tests.data_manager.factory.readers.kaist.conftest import DATASET_CONFIG_NAME, REGIME_CONFIG_NAME

from .data import (
    DatasetStructure,
    data_stamp,
    stamp_files,
    csv_data,
    binary_data,
    image_data)

from .config import KaistReaderConfig


@fixture(scope='class', autouse=True)
def register_configs() -> None:
    cs = ConfigStore.instance()
    cs.store(name=DATASET_CONFIG_NAME, node=KaistReaderConfig)
    cs.store(name=REGIME_CONFIG_NAME, node=StreamConfig)


@fixture(scope="class", autouse=True)
def generate_dataset():
    data_factory = DataFactory(DatasetStructure())
    data_factory.create_dataset_structure()
    data_factory.generate_data(
        data_stamp,
        stamp_files,
        csv_data,
        binary_data,
        image_data)


@fixture(scope='class', autouse=True)
def clean():
    yield
    rmtree(DatasetStructure.dataset_directory)
