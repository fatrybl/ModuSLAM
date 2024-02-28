from shutil import rmtree

from pytest import fixture

from tests_data.kaist_urban_dataset.data import DATASET_DIR as kaist_dataset_directory
from tests_data.kaist_urban_dataset.kaist_data_factory import (
    DataFactory as KaistDataFactory,
)
from tests_data.kaist_urban_dataset.structure import DatasetStructure


@fixture(scope="package", autouse=True)
def kaist_urban_dataset() -> None:
    """Generates Kaist Urban Dataset with the predefined data."""
    structure = DatasetStructure(dataset_directory=kaist_dataset_directory)
    data_factory = KaistDataFactory(structure)
    data_factory.generate_data()


@fixture(scope="package", autouse=True)
def clean():
    yield
    rmtree(kaist_dataset_directory)
