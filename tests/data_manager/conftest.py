from shutil import rmtree

from pytest import fixture

from tests.conftest import kaist_custom_dataset_dir
from tests_data_generators.kaist_dataset.data import Data
from tests_data_generators.kaist_dataset.factory import DataFactory


@fixture(scope="package", autouse=True)
def generate_kaist_urban_dataset() -> None:
    data = Data(kaist_custom_dataset_dir)
    data_factory = DataFactory(data)
    data_factory.generate_data()


@fixture(scope="package", autouse=True)
def clean():
    yield
    rmtree(kaist_custom_dataset_dir)
