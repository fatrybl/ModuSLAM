from shutil import rmtree

from hydra.core.config_store import ConfigStore
from pytest import fixture

from configs.system.data_manager.batch_factory.regime import StreamConfig
from tests.data_manager.auxiliary_utils.kaist_data_factory import DataFactory
from tests.data_manager.factory.readers.kaist.api.empty_dataset.config import (
    KaistReaderConfig,
)
from tests.data_manager.factory.readers.kaist.api.empty_dataset.data import (
    DatasetStructure,
)
from tests.data_manager.factory.readers.kaist.conftest import (
    DATASET_CONFIG_NAME,
    REGIME_CONFIG_NAME,
)


@fixture(scope="class", autouse=True)
def register_configs() -> None:
    cs = ConfigStore.instance()
    cs.store(name=DATASET_CONFIG_NAME, node=KaistReaderConfig)
    cs.store(name=REGIME_CONFIG_NAME, node=StreamConfig)


@fixture(scope="class", autouse=True)
def generate_dataset() -> None:
    data_factory = DataFactory(DatasetStructure())
    data_factory.create_dataset_structure()


@fixture(scope="class", autouse=True)
def clean():
    yield
    rmtree(DatasetStructure.dataset_directory)
